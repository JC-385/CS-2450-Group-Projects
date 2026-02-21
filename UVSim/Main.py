from Simulator import BasicMLSimulator
from GUI import getEntryValue, run_gui

def main():
    simulator = BasicMLSimulator()

    filename = getEntryValue("file")
    simulator.load_program(filename)
    simulator.run()

    run_gui()

if __name__ == "__main__":
    main()
