"""UVSim entry point.

This module launches the UVSim BasicML virtual machine simulator with the
tkinter-based graphical user interface.
"""

from Simulator import BasicMLSimulator
from Gui import run_gui


def main():
    """Launch the UVSim GUI application.
    
    Initializes and displays the tkinter-based user interface, which allows
    users to open, edit, and execute BasicML programs.
    """
    run_gui()


if __name__ == "__main__":
    main()
     