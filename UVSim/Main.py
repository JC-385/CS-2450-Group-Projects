from Operators import *
#Global dictionary for the memory
memory = {}
list_of_lines = []
File = input("Enter the file name: ")
with open (File, "r") as file:
    for line in file:
        list_of_lines.append(line)
print(list_of_lines)

for line in list_of_lines:
    operator = line[1:2]
    match operator:
        case "10":
            memory = READ(line[3:], memory)
        case "11":
            memory = WRITE(line[3:], memory)
        case "20":
            memory = LOAD(line[3:], memory)
        case "21":
            memory = STORE(line[3:], memory)
        case "30":
            memory = ADD(line[3:], memory)
        case "31":
            memory = SUBTRACT(line[3:], memory)
        case "32":
            memory = DIVIDE(line[3:], memory)
        case "33":
            memory = MULTIPLY(line[3:], memory)
        case "40":
            BRANCH(line[3:], memory)
        case "41":
            BRANCHNEG(line[3:], memory)
        case "42":
            BRANCHZERO(line[3:], memory)
        case "43":
            HALT(line[3:], memory)