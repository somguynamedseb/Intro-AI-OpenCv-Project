import PySimpleGUI as sg
import img_viewer

s = 1500

def get_home_layout():
    return [[sg.Column([[sg.Text('Welcome!',font=('Helvetica', 50),
                                 border_width=20, key='-home-')]],
                       vertical_alignment='center', justification='center')]]
