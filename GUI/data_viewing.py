import PySimpleGUI as sg


def get_data_layout():
    inputs = [
        [sg.Text("Total Data", font=('Helvetica', 30))],
        [sg.Text("", size=(0, 5))],
        [sg.Graph(canvas_size=(700, 200), graph_bottom_left=(0, 0), graph_top_right=(200, 700),
                  background_color='white', key='-GRAPH-')],
    ]

    # Add a total students scanned and at what confidence rate objects

    # ----- Full layout -----
    layout = [
        [sg.Column(inputs, justification='center', vertical_alignment='center'),
         ]
    ]
    return layout
