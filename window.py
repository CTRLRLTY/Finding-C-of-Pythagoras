import PySimpleGUI as sg
from constant import *

RUN_OUTPUT_BGCOLOR = "red"
RUN_ELEM_COLOR = "BLUE"

RUN_ELEMENTS = [[sg.Text(size=(40,1), key=k, pad=(0,0), background_color=RUN_ELEM_COLOR)] for k in RUN_OUTPUT.values()]

RUN_OUTPUT_DIV = sg.Column([*RUN_ELEMENTS],background_color=RUN_OUTPUT_BGCOLOR)

layout = [
  [sg.Text("Input N (int)")],
  [sg.Input(size=(40,1), key=INPUT_N)],
  [sg.Text("Input Precisiion (int)")],
  [sg.Input(size=(40,1), key=INPUT_DPS)],
  [RUN_OUTPUT_DIV],
  [sg.Button(BUTTON_RUN)],
]

window = sg.Window('something', layout, margins=(0,0))

RUN_OUTPUT_WIN = {
  "Progress": window[RUN_OUTPUT["Progress"]],
  "I": window[RUN_OUTPUT["I"]],
  "B": window[RUN_OUTPUT["B"]],
  "C": window[RUN_OUTPUT["C"]],
  "C^2": window[RUN_OUTPUT["C^2"]],
  "A^2": window[RUN_OUTPUT["A^2"]],
  "A": window[RUN_OUTPUT["A"]],
}