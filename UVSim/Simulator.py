from Operators import *

class BasicMLSimulator:
    def __init__(self):
        self.memory = [0] * 100
        self.accumulator = 0
        self.pc = 0
        self.halted = False
        self.program = []
        self.op = Operators()

    def load_program(self, filename):
        with open(filename, "r") as file:
            self.program = [line.strip() for line in file]

    def step(self):
        self.memory 
        if self.pc >= len(self.program) or self.halted:
            return
        line = self.program[self.pc]
        opcode = line[1:3]
        address = int(line[3:5])

        match opcode:
            case "10":
                self.op.READ(address, self.memory)
            case "11":
                self.op.WRITE(address, self.memory)
            case "20":
                self.accumulator = self.op.LOAD(address, self.memory)
            case "21":
                self.op.STORE(address, self.memory, self.accumulator)
            case "30":
                self.accumulator = self.op.ADD(address, self.memory, self.accumulator)
            case "31":
                self.accumulator = self.op.SUBTRACT(address, self.memory, self.accumulator)
            case "32":
                self.accumulator = self.op.DIVIDE(address, self.memory, self.accumulator)
            case "33":
                self.accumulator = self.op.MULTIPLY(address, self.memory, self.accumulator)
            case "40":
                self.pc = self.op.BRANCH(address)
                return
            case "41":
                new_pc = self.op.BRANCHNEG(address, self.accumulator)
                if new_pc is not None:
                    self.pc = new_pc
                    return
            case "42":
                new_pc = self.op.BRANCHZERO(address, self.accumulator)
                if new_pc is not None:
                    self.pc = new_pc
                    return
            case "43":
                self.halted = self.op.HALT()
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