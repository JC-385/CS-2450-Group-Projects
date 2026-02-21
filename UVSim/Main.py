from Operators import *
from Gui import *
#Global dictionary for the memory

def main():
    memory = [0]*100
    accumulator = 0 
    pc = 0
    halted = False
    list_of_lines = []
    File = getEntryValue("file")
    with open (File, "r") as file:
        for line in file:
            list_of_lines.append(line)
    print(list_of_lines)

    while pc < len(list_of_lines) and not halted:
        line = list_of_lines[pc].strip()
        opcode = line[1:3]
        address = int(line[3:5])
        match opcode:
            case "10":
                READ(address, memory)
            case "11":
                WRITE(address, memory)
            case "20":
                accumulator = LOAD(address, memory)
            case "21":
                STORE(address, memory, accumulator)
            case "30":
                accumulator = ADD(address, memory, accumulator)
            case "31":
                accumulator = SUBTRACT(address, memory,accumulator)
            case "32":
                accumulator = DIVIDE(address, memory,accumulator)
            case "33":
                accumulator = MULTIPLY(address, memory,accumulator)
            case "40":
                BRANCH(address)
                continue
            case "41":
                new_pc = BRANCHNEG(address, accumulator)
                if new_pc is not None:
                    pc = new_pc
                    continue
            case "42":
                new_pc = BRANCHZERO(address, accumulator)
                if new_pc is not None:
                    pc = new_pc
                    continue
            case "43":
                halted = HALT()
            case _:
                print("Invalid operator")

        pc += 1

    run_gui()  # Keep window open after simulation (or remove to close immediately)

if __name__ == "__main__":
    main()