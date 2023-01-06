"""Calculate arithmetic expressions from GUI."""
import PySimpleGUI

import package_name_to_import_with


def define_gui_layout() -> list[list[PySimpleGUI.Element]]:
    """Prepare design of the GUI.

    Returns
    -------
    list[list[PySimpleGUI.Element]]
        elements of the GUI
    """
    layout = [
        [PySimpleGUI.Text("Enter first number"), PySimpleGUI.Input(key="first_number")],
        [
            PySimpleGUI.Text("Enter operator"),
            PySimpleGUI.OptionMenu(["+", "-", "*", "/"], key="operator"),
        ],
        [PySimpleGUI.Text("Enter second number"), PySimpleGUI.Input(key="second_number")],
        [PySimpleGUI.Button(button_text="Submit")],
        [PySimpleGUI.Text("Operation Result", key="result")],
        [PySimpleGUI.Button(button_text="Close")],
    ]

    return layout


def define_gui_window(gui_layout: list[list[PySimpleGUI.Element]]) -> PySimpleGUI.Window:
    """Create GUI with provided design.

    Parameters
    ----------
    gui_layout : list[list[PySimpleGUI.Element]]
        design of the GUI

    Returns
    -------
    PySimpleGUI.Window
        designed GUI
    """
    window = PySimpleGUI.Window("GUI Calculator", layout=gui_layout)

    return window


def orchestrate_interaction(gui_window: PySimpleGUI.Window) -> None:
    """Control flow of the GUI.

    Parameters
    ----------
    gui_window : PySimpleGUI.Window
        designed GUI
    """
    while True:  # pylint: disable=while-used
        gui_event, gui_elements = gui_window.read()

        if PySimpleGUI.WINDOW_CLOSED or gui_event == "Close":
            break

        try:
            operation_result = package_name_to_import_with.calculate_results(
                gui_elements["first_number"],
                gui_elements["operator"],
                gui_elements["second_number"],
            )
        except Exception as error:  # pylint: disable=broad-except
            gui_window["result"].update(error)
        else:
            gui_window["result"].update(operation_result)


def gui_calculator() -> None:
    """Calculate arithmetic expressions."""
    gui_layout = define_gui_layout()
    gui_window = define_gui_window(gui_layout)

    try:
        orchestrate_interaction(gui_window)
    finally:
        gui_window.close()


if __name__ == "__main__":
    gui_calculator()
