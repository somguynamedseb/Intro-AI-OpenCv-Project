from PIL import Image, ImageTk
import io

import home
import img_viewer
import input_page
import image_manager
import os.path

import cv2
import PySimpleGUI as sg
from io import BytesIO
from ultralytics import YOLO

# ----------- Create the 3 layouts this Window will display -----------
layout1 = home.get_home_layout()

layout2 = img_viewer.img_viewer_layout()

layout3 = input_page.get_input_layout()

# ----------- Create actual layout using Columns and a row of Buttons
layout = [
    [sg.Button('Exit', font=('Helvetica', 15), size=10, key='-EXIT-')],
    [sg.Column([[
        sg.Button('Back', key='-BACK-', font=('Helvetica', 15), size=10),
        sg.Button('Next', key="-NEXT-", font=('Helvetica', 15), size=10), ]],
        key='-BUTTONS-', vertical_alignment='bottom', justification='center')],
    [sg.Column([[sg.Text("", size=(0, 5))]], vertical_alignment='center', justification='center')],
    [sg.Column(layout1, visible=True, key='-COL1-', vertical_alignment='center', justification='center'),
     sg.Column(layout2, visible=False, key='-COL2-', vertical_alignment='center', justification='center'),
     sg.Column(layout3, visible=False, key='-COL3-', vertical_alignment='center', justification='center'), ],
    [sg.Button('Full Screen', font=('Helvetica', 15), size=10, key='-FSCREEN-')],
]

window = sg.Window('Attendance-AI', layout, finalize=True)
window.maximize()


def main():
    stitchImgs = []
    imgClicked = ""
    confidenceScan = 0.60
    maxPages = 3
    page = 1  # The currently visible layout
    im = image_manager.image_manager
    readyScanImage: bytes = ""
    window[f'-BACK-'].update(visible=False)
    while True:
        event, values = window.read()
        # print("PAGE: " + str(page))
        if event in (None, "-EXIT-"):
            break
        elif event == sg.WIN_CLOSED:
            break
        elif event == "-BACK-":
            if page > 1:
                window[f'-BACK-'].update(visible=True)
                window[f'-NEXT-'].update(visible=True)
                window[f'-COL{page}-'].update(visible=False)
                page -= 1
                if page == 1:
                    window[f'-BACK-'].update(visible=False)
                window[f'-COL{page}-'].update(visible=True)
        elif event == "-NEXT-":
            if 0 < page < maxPages:
                window[f'-BACK-'].update(visible=True)
                window[f'-COL{page}-'].update(visible=False)
                page += 1
                window[f'-COL{page}-'].update(visible=True)
                window[f'-NEXT-'].update(visible=False)
        elif event == "-FOLDER-":
            folder = values["-FOLDER-"]
            try:
                # Get list of files in folder
                file_list = os.listdir(folder)
            except:
                file_list = []

            fnames = [
                f
                for f in file_list
                if os.path.isfile(os.path.join(folder, f))
                   and f.lower().endswith((".png", ".gif", ".jpg"))
            ]
            window["-FILE LIST-"].update(fnames)
        elif event == "-FILE LIST-":  # A file was chosen from the listbox
            try:
                filename = os.path.join(values["-FOLDER-"], values["-FILE LIST-"][0])
                if os.path.exists(filename):  # Check if the file exists
                    data = find_data_from_dir(filename)
                    # Update the GUI to display the resized image
                    window["-TOUT-"].update(filename)
                    window["-IMAGE-"].update(data=data)
                    # Make the '-ADD-' button visible
                    window["-ADD-"].update(visible=True)
                    imgClicked = filename
                else:
                    sg.popup_error(f"File not found: {filename}")
            except Exception as e:
                sg.popup_error(f"An error occurred: {e}")
        elif event == "-RESET-":
            window["-FILE LIST-"].update([])
            window["-ADDED IMGS-"].update([])
            window["-TOUT-"].update("")
            window["-IMAGE-"].update(filename="")
            window["-FOLDER-"].update("")
            window[f'-ADD-'].update(visible=False)
            window[f'-STITCH-'].update(visible=False)
            window[f'-NEXT-'].update(visible=False)
            window[f'-SKIP-'].update(visible=False)
            window[f'-IMGTEXT-'].update("Chosen Image from the left:")
            window['-NUM STUDENTS-'].update([])
            window['-NUM EXEMPTIONS-'].update([])
            stitchImgs.clear()
            readyScanImage = ''
        elif event == "-ADD-":
            stitchImgs.insert(stitchImgs.__len__(), imgClicked)
            window["-ADDED IMGS-"].update(stitchImgs)

            if stitchImgs.__len__() == 1:
                window["-SKIP-"].update(visible=True)
            elif stitchImgs.__len__() > 1:
                window["-SKIP-"].update(visible=False)
                window[f'-STITCH-'].update(visible=True)
            # possibly make a delete function for added stitched imgs
        elif event == "-SKIP-":
            window[f'-COL{page}-'].update(visible=False)
            page = maxPages
            window[f'-COL{page}-'].update(visible=True)
            window[f'-NEXT-'].update(visible=False)

            filename = stitchImgs[0]
            if os.path.exists(filename):  # Check if the file exists
                img = find_data_from_dir(filename)
                window["-TOUT-"].update(filename)
                window["-IMAGE-"].update(data=img)
                readyScanImage = img

        elif event == "-STITCH-":
            if len(stitchImgs) >= 2:  # Ensure there are at least two images to stitch
                # LINK TO AI SCAN FUNCTION
                im.add_image_list(im, stitchImgs)
                imgBytes = im.stitch_images(im)
                window["-IMAGE-"].update(data='')
                readyScanImage = imgBytes

                window[f'-IMGTEXT-'].update("Successfully Stitched!")
                window[f'-TOUT-'].update("")
                window["-SKIP-"].update(visible=False)
                window[f'-NEXT-'].update(visible=True)
                window[f'-STITCH-'].update(visible=False)
                window["-ADD-"].update(visible=False)
                window["-FILE LIST-"].update([])
                window["-FOLDER-"].update("")
            else:
                sg.popup_error('Need at least two images to stitch!')
        elif event == "-CALCULATE-":
            sImgDir, scannedStudents = detect_faces(readyScanImage)
            try:
                vS = values['-NUM STUDENTS-']
                vE = values['-NUM EXEMPTIONS-']
                num_students = int(vS)
                num_exemptions = int(vE)
                # if everyone is in the class then num_students and scannedStudents should be equal
                total_student = num_students - num_exemptions - (num_students - scannedStudents)
                percentage: int = total_student / num_students * 100
                rounded_percent = round(percentage, 2)
                print(str(rounded_percent))

                # scannedImgBytes = find_data_from_dir(sImgDir)
                window["-SCANNED IMAGE-"].update(data=readyScanImage)
                window[f'-PERCENTAGE-'].update(str(rounded_percent) + "%")
            except:
                sg.popup_error("Please Enter A Valid Number")

    window.close()


def find_data_from_dir(filename):
    # Open the image file using Pillow
    image = Image.open(filename)
    # Define the size to which you want to scale the image
    max_width, max_height = 400, 300  # Adjust these values as needed
    # Calculate the scaling factor, maintaining the aspect ratio
    scaling_factor = min(max_width / image.width, max_height / image.height)
    # Compute the new size
    new_size = (int(image.width * scaling_factor), int(image.height * scaling_factor))
    # Resize the image
    image = image.resize(new_size, Image.Resampling.LANCZOS)
    # Save the resized image to a BytesIO object
    bio = io.BytesIO()
    image.save(bio, format="PNG")
    bio.seek(0)
    return bio.read()


def detect_faces(imgDIR) -> [str, int]:  # returns DIR of output img
    model = YOLO('train3/weights/last.pt')
    if isinstance(imgDIR, bytes):
        img = Image.open(BytesIO(imgDIR))
    else:
        img = Image.open(imgDIR)
    results = model.predict(source=img, save=True)  # save plotted images
    result = results[0]
    detected_img = str(result.save_dir)
    face_count = len(result.boxes.xyxy)
    detected_img = detected_img.replace("\\", "/")
    return [detected_img, face_count]


if __name__ == "__main__":
    main()
