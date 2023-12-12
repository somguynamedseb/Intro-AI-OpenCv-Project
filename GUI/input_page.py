import PySimpleGUI as sg


def get_input_layout():
    inputs = [
        [sg.Text("Total Number Of Students", font=('Helvetica', 30))],
        [sg.Input("0", key='-NUM_STUDENTS-', font=('Helvetica', 15), size=15, pad=(150, 0))],
        [sg.Text("", size=(0, 2))],
        [sg.Text("Number Of Exemptions", font=('Helvetica', 30))],
        [sg.Input("0", key='-NUM_EXEMPTIONS-', font=('Helvetica', 15), size=15, pad=(150, 0))],
        [sg.Text("", size=(0, 5))],
        [sg.Button("Calculate", font=('Helvetica', 15), size=15, pad=(150, 0), key="-CALCULATE-")],
        [sg.Text("", size=(0, 1))],
        [sg.Text("00.00%", background_color='navyblue', text_color='white', key='-PERCENTAGE-', font=('Helvetica', 15),
                 size=8, pad=(190, 0), justification='center')]
    ]

    image_viewer_column = [
        [sg.Text("Post-Scanned Image:", font=('Helvetica', 30), key='-IMGTEXT-')],
        [sg.Text(font=('Helvetica', 10), size=(30, 5), key="-TOUT-")],
        [sg.Image(key="-SCANNED IMAGE-")], ]
    # Add a total students scanned and at what confidence rate objects

    # ----- Full layout -----
    layout = [
        [sg.Column(image_viewer_column),
         sg.VSeperator(),
         sg.Column(inputs),
         ]
    ]
    return layout
