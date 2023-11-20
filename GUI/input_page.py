import PySimpleGUI as sg


def get_input_layout():
    inputs = [
        [sg.Text("Total Number Of Students", font=('Helvetica', 30))],
        [sg.Input(key='-NUM_STUDENTS-', font=('Helvetica', 15))],
        [sg.Text("Number Of Exemptions", font=('Helvetica', 30))],
        [sg.Input(key='-NUM_EXEMPTIONS-', font=('Helvetica', 15))],
        [sg.Button("Calculate", font=('Helvetica', 15), size=(10, 1))]
    ]

    # ----- Full layout -----
    layout = [
        [sg.Column(inputs, vertical_alignment='center', justification='center')]
    ]
    return layout


