# img_viewer.py

import PySimpleGUI as sg
import os.path
import home
import input_page


def img_viewer_layout():
    file_list_column = [
        [sg.Text("Image Folder", font=('Helvetica', 30)),
         sg.In(size=(40, 1), enable_events=True, key="-FOLDER-"),
         sg.FolderBrowse(), ],
        [sg.Listbox(
            values=[], font=('Helvetica', 15), enable_events=True, size=(40, 20), key="-FILE LIST-")],
    ]

    # For now will only show the name of the file that was chosen
    image_viewer_column = [
        [sg.Text("Chosen Image from the left:", font=('Helvetica', 30))],
        [sg.Text(font=('Helvetica', 15), size=(50, 5), key="-TOUT-")],
        [sg.Image(key="-IMAGE-")],
    ]

    # ----- Full layout -----
    column_to_be_centered = [
        [sg.Column(file_list_column), sg.VSeperator(),
         sg.Column(image_viewer_column)],
        [sg.Button("Reset", font=('Helvetica', 15), size=10, key="-RESET-")],
        [sg.Button("Add", font=('Helvetica', 15), size=10, key="-ADD-", visible=False)],
        [sg.Button("Stitch", font=('Helvetica', 15), size=10, key="-STITCH-", visible=False)],
    ]
    return [[sg.Column(column_to_be_centered, vertical_alignment='center', justification='center')]]
