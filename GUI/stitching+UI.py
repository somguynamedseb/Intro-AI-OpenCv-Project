import home
import img_viewer
import input_page
import os.path

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
                   and f.lower().endswith((".png", ".gif"))
            ]
            window["-FILE LIST-"].update(fnames)
        elif event == "-FILE LIST-":  # A file was chosen from the listbox
            try:
                filename = os.path.join(
                    values["-FOLDER-"], values["-FILE LIST-"][0]
                )
                window["-TOUT-"].update(filename)
                window["-IMAGE-"].update(filename=filename)
                window[f'-ADD-'].update(visible=True)
                imgClicked = filename
            except:
                pass
        elif event == "-RESET-":
            window["-FILE LIST-"].update([])
            window["-ADDED IMGS-"].update([])
            window["-TOUT-"].update("")
            window["-IMAGE-"].update(filename="")
            window["-FOLDER-"].update("")
            window[f'-ADD-'].update(visible=False)
            window[f'-STITCH-'].update(visible=False)
            window[f'-NEXT-'].update(visible=False)
            stitchImgs.clear()
        elif event == "-ADD-":
            s = stitchImgs.__len__()
            stitchImgs.insert(s, imgClicked)
            window[f'-STITCH-'].update(visible=True)
            window["-ADDED IMGS-"].update(stitchImgs)
        # delete function for added stitched imgs
        elif event == "-STITCH-":
            # stitching.updateImgs(stitchImgs)
            # stitching.run()
            window[f'-IMGTEXT-'].update("Stitched Image:")
            window[f'-TOUT-'].update("")
            # window[f'-IMAGE-'].update(stitchedImg)
            window[f'-NEXT-'].update(visible=True)
            print("Stitched " + str(stitchImgs.__len__()) + " images.")
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
