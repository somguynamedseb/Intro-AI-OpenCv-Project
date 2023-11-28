import PySimpleGUI as sg


def get_input_layout():
    inputs = [
        [sg.Text("Total Number Of Students", font=('Helvetica', 30))],
        [sg.Input(key='-NUM_STUDENTS-', font=('Helvetica', 15), size=15, pad=(150, 0))],
        [sg.Text("", size=(0, 2))],
        [sg.Text("Number Of Exemptions", font=('Helvetica', 30))],
        [sg.Input(key='-NUM_EXEMPTIONS-', font=('Helvetica', 15), size=15, pad=(150, 0))],
        [sg.Text("", size=(0, 5))],
        [sg.Button("Calculate", font=('Helvetica', 15), size=15, pad=(150, 0))]
    ]

    # ----- Full layout -----
    layout = [
        [sg.Column(inputs, vertical_alignment='center', justification='center',),
         ]
    ]
    return layout


