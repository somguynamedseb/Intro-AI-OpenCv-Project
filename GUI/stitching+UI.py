
from PIL import Image, ImageTk
import io


import home
import img_viewer
import input_page
import os.path

import cv2
import PySimpleGUI as sg

# ----------- Create the 3 layouts this Window will display -----------
layout1 = home.get_home_layout()

layout2 = img_viewer.img_viewer_layout()

layout3 = input_page.get_input_layout()


stitchImgs = []

imgClicked = ""

# ----------- Create actual layout using Columns and a row of Buttons
layout = [
    [sg.Button('Exit', font=('Helvetica', 15), size=10)],
    [sg.Column([[
        sg.Button('Back', key='-BACK-', font=('Helvetica', 15), size=10),
        sg.Button('Next', key="-NEXT-", font=('Helvetica', 15), size=10)]],
        key='-BUTTONS-', vertical_alignment='bottom', justification='center')],
    [sg.Column([[sg.Text("", size=(0, 5))]], vertical_alignment='center', justification='center')],
    [sg.Column(layout1, visible=True, key='-COL1-', vertical_alignment='center', justification='center'),
     sg.Column(layout2, visible=False, key='-COL2-', vertical_alignment='center', justification='center'),
     sg.Column(layout3, visible=False, key='-COL3-', vertical_alignment='center', justification='center'),],
]

window = sg.Window('Attendance-AI', layout, finalize=True)
window.maximize()


# home.windowUpdate(window)

def main():
    global imgClicked
    maxPages = 3
    page = 1  # The currently visible layout
    window[f'-BACK-'].update(visible=False)
    while True:
        event, values = window.read()
        # print("PAGE: " + str(page))
        if event in (None, 'Exit'):
            break
        if event == sg.WIN_CLOSED:
            break

        if event == "-BACK-":
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
                if page == maxPages:
                    window[f'-NEXT-'].update(visible=False)
                window[f'-COL{page}-'].update(visible=True)
                window[f'-NEXT-'].update(visible=False)
        if event == "-FOLDER-":
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
                    # Update the GUI to display the resized image
                    window["-TOUT-"].update(filename)
                    window["-IMAGE-"].update(data=bio.read())
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
            window[f'-IMGTEXT-'].update("Chosen Image from the left:")
            stitchImgs.clear()
        elif event == "-ADD-":
            s = stitchImgs.__len__()
            stitchImgs.insert(s, imgClicked)
            window[f'-STITCH-'].update(visible=True)
            window["-ADDED IMGS-"].update(stitchImgs)
        # delete function for added stitched imgs
        elif event == "-STITCH-":
            if len(stitchImgs) >= 2:  # Ensure there are at least two images to stitch
                # Read images and store them in a list
                images = [cv2.imread(img) for img in stitchImgs]
                # Create a stitcher object
                stitcher = cv2.Stitcher.create()
                # Perform the stitching process
                status, stitched_img = stitcher.stitch(images)
                if status == cv2.Stitcher_OK:
                    # Convert the stitched image to a PIL Image
                    stitched_pil_image = Image.fromarray(cv2.cvtColor(stitched_img, cv2.COLOR_BGR2RGB))
                    # Define the size to which you want to scale the image
                    max_width, max_height = 400, 300  # Adjust these values as needed
                    # Calculate the scaling factor, maintaining the aspect ratio
                    scaling_factor = min(max_width / stitched_pil_image.width, max_height / stitched_pil_image.height)
                    # Compute the new size
                    new_size = (int(stitched_pil_image.width * scaling_factor), int(stitched_pil_image.height * scaling_factor))
                    # Resize the image
                    stitched_pil_image = stitched_pil_image.resize(new_size, Image.Resampling.LANCZOS)
                    # Save the resized image to a BytesIO object
                    bio = io.BytesIO()
                    stitched_pil_image.save(bio, format="PNG")
                    bio.seek(0)
                    # Update the GUI to display the resized stitched image
                    window[f'-IMGTEXT-'].update("Stitched Image:")
                    window[f'-TOUT-'].update("")
                    window[f'-NEXT-'].update(visible=True)
                    print("Stitched " + str(stitchImgs.__len__()) + " images.")
                else:
                    sg.popup_error('Image stitching failed!', 'Error code: ' + str(status))
            else:
                sg.popup_error('Need at least two images to stitch!')
        else:
            pass

        if event == "-CALCULATE-":
            num_students = int(values['-NUM_STUDENTS-'])
            num_exemptions = int(values['-NUM_EXEMPTIONS-'])
            total_student = num_students - num_exemptions
            print("Total Number Of Students In Class: " + str(total_student))

    window.close()


if __name__ == "__main__":
    main()

