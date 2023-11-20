import PySimpleGUI as sg
import img_viewer

s = 1500


# def windowUpdate(window):
#     window['-C-'].expand(True, True, True)
#     window['-EXPAND-'].expand(True, True, True)
#     window['-EXPAND2-'].expand(True, False, True)
#     window.maximize()
#
#
# def home_page_layout():
#     column_to_be_centered = [[sg.Button('Start Attendance', font=('Helvetica', 50), border_width=20, key='-home-')]]
#     return [[sg.Text('Welcome!', font=('Helvetica', 80), justification='center')],
#             [sg.Text(key='-EXPAND-', font='ANY 1', pad=(0, 0))],
#             [sg.Text('', pad=(0, 0), key='-EXPAND2-'),
#              sg.Column(column_to_be_centered, vertical_alignment='center', justification='center', k='-C-')]]


def get_home_layout():
    return [[sg.Column([[sg.Text('Welcome!',font=('Helvetica', 50),
                                 border_width=20, key='-home-')]],
                       vertical_alignment='center', justification='center')]]
