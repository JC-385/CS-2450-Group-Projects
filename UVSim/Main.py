from email.headerregistry import Address
from Operators import *
#Global dictionary for the memory
memory = [0]*100
accumulator = 0

list_of_lines = []
File = input("Enter the file name: ")
with open (File, "r") as file:
    for line in file:
        list_of_lines.append(line)
print(list_of_lines)

for line in list_of_lines:
    opcode = line[1:3]
    address = int(line[3:5])
    match opcode:
        case "10":
            memory = READ(address, memory)
        case "11":
            memory = WRITE(address, memory)
        case "20":
            memory = LOAD(address, memory)
        case "21":
            memory = STORE(address, memory, accumulator)
        case "30":
            memory = ADD(address, memory)
        case "31":
            memory = SUBTRACT(address, memory)
        case "32":
            memory = DIVIDE(address, memory)
        case "33":
            memory = MULTIPLY(address, memory)
        case "40":
            BRANCH(address, memory)
        case "41":
            BRANCHNEG(address, memory)
        case "42":
            BRANCHZERO(address, memory)
        case "43":
            HALT(address, memory)
        case _:
            print("Invalid operator")