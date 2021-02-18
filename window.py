import PySimpleGUI as sg
from constant import *

RUN_OUTPUT_BGCOLOR = "red"
RUN_ELEM_COLOR = "#94538a"

RUN_ELEMENTS = [[sg.Text(size=(40,1), key=k, pad=(0,0), background_color=RUN_ELEM_COLOR)] for k in RUN_OUTPUT.values()]

RUN_OUTPUT_DIV = sg.Column([*RUN_ELEMENTS],background_color=RUN_OUTPUT_BGCOLOR)

layout = [
  [sg.Text("Input N (Required: int)")],
  [sg.Input(size=(40,1), key=INPUT_N)],
  [sg.Text("Input Percision (Required: int)")],
  [sg.Input(size=(40,1), key=INPUT_DPS)],
  [sg.Text("Input I (Optional: int)")],
  [sg.Input(size=(40, 1), key=INPUT_I)],
  [RUN_OUTPUT_DIV],
  [sg.Button(BUTTON_RUN), sg.Button(BUTTON_STOP)],
]

window = sg.Window('something', layout, margins=(0,0))

INPUT_DPS_WIN = window[INPUT_DPS]

RUN_OUTPUT_WIN = {
  "Progress": window[RUN_OUTPUT["Progress"]],
  "I": window[RUN_OUTPUT["I"]],
  "B": window[RUN_OUTPUT["B"]],
  "C": window[RUN_OUTPUT["C"]],
  "C^2": window[RUN_OUTPUT["C^2"]],
  "A^2": window[RUN_OUTPUT["A^2"]],
  "A": window[RUN_OUTPUT["A"]],
  "P": window[RUN_OUTPUT["P"]],
  "Q": window[RUN_OUTPUT["Q"]]
}