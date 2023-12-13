# img_viewer.py

import PySimpleGUI as sg


def img_viewer_layout():
    file_list_column = [
        [sg.Text("Image Folder", font=('Helvetica', 30), key='-TEXT IMG FOLDER-'),
         sg.In(size=(40, 1), enable_events=True, key="-FOLDER-"),
         sg.FolderBrowse(key='-FBROWSE-')],
        [sg.Listbox(
            values=[], font=('Helvetica', 15), enable_events=True, size=(30, 15), key="-FILE LIST-")],
        [sg.Text("Current Stitching List: ", font=('Helvetica', 20))],
        [sg.Listbox(values=[], key="-ADDED IMGS-", font=('Helvetica', 10), size=(45, 10), enable_events=True)]
    ]

    # For now will only show the name of the file that was chosen
    image_viewer_column = [
        [sg.Text("Chosen Image from the left:", font=('Helvetica', 30), key='-IMGTEXT-')],
        [sg.Text(font=('Helvetica', 10), size=(30, 5), key="-TOUT-")],
        [sg.Image(key="-IMAGE-")], ]

    # ----- Full layout -----
    column_to_be_centered = [
        [sg.Column(file_list_column, key='-LISTCOL-'), sg.VSeperator(),
         sg.Column(image_viewer_column),
         sg.Column([
             [sg.Button("Reset", font=('Helvetica', 15), size=10, key="-RESET-")],
             [sg.Button("Add", font=('Helvetica', 15), size=10, key="-ADD-", visible=False)],
             [sg.Button("Stitch", font=('Helvetica', 15), size=10, key="-STITCH-", visible=False)],
             [sg.Button("Skip Stitching", font=('Helvetica', 15), size=15, key="-SKIP-", visible=False)],
         ])]
    ]
    return [[sg.Column(column_to_be_centered, vertical_alignment='center', justification='center')]]
