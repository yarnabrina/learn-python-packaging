import PySimpleGUI

FIRST_NUMBER_INPUT: str
SECOND_NUMBER_INPUT: str
OPERATOR_INPUT: str
OPERATION_RESULT: str
CLOSE_BUTTON: str

def define_gui_layout() -> list[list[PySimpleGUI.Element]]: ...
def define_gui_window(gui_layout: list[list[PySimpleGUI.Element]]) -> PySimpleGUI.Window: ...
def orchestrate_interaction(gui_window: PySimpleGUI.Window) -> None: ...
def gui_calculator() -> None: ...
