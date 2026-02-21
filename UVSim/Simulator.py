from Operators import *

class BasicMLSimulator:
    def __init__(self):
        self.memory = [0] * 100
        self.accumulator = 0
        self.pc = 0
        self.halted = False
        self.program = []

    def load_program(self, filename):
        with open(filename, "r") as file:
            self.program = [line.strip() for line in file]

    def step(self):
        if self.pc >= len(self.program) or self.halted:
            return

        line = self.program[self.pc]
        opcode = line[1:3]
        address = int(line[3:5])

        match opcode:
            case "10":
                READ(address, self.memory)
            case "11":
                WRITE(address, self.memory)
            case "20":
                self.accumulator = LOAD(address, self.memory)
            case "21":
                STORE(address, self.memory, self.accumulator)
            case "30":
                self.accumulator = ADD(address, self.memory, self.accumulator)
            case "31":
                self.accumulator = SUBTRACT(address, self.memory, self.accumulator)
            case "32":
                self.accumulator = DIVIDE(address, self.memory, self.accumulator)
            case "33":
                self.accumulator = MULTIPLY(address, self.memory, self.accumulator)
            case "40":
                self.pc = BRANCH(address)
                return
            case "41":
                new_pc = BRANCHNEG(address, self.accumulator)
                if new_pc is not None:
                    self.pc = new_pc
                    return
            case "42":
                new_pc = BRANCHZERO(address, self.accumulator)
                if new_pc is not None:
                    self.pc = new_pc
                    return
            case "43":
                self.halted = HALT()
            case _:
                print("Invalid operator")

        self.pc += 1

    def run(self):
        while not self.halted and self.pc < len(self.program):
            self.step()

    def reset(self):
        self.memory = [0] * 100
        self.accumulator = 0
        self.pc = 0
        self.halted = False
        self.program = []