class BasicMLSimulator:
    def __init__(self, input_func, output_func):
        self.acc = 0
        self.memory = [0] * 250     # 250 memory addresses
        self.pc = 0                 # program counter
        self.program = []
        self.halted = False

        self.input_func = input_func
        self.output_func = output_func

    def load_program(self, filename):
        """Load file into self.program list."""
        self.program = []
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    self.program.append(line)

        self.pc = 0
        self.halted = False

    def step(self):
        """Execute a single instruction."""
        if self.halted or self.pc >= len(self.program):
            return

        line = self.program[self.pc]

        # Program counter always increments unless a branch occurs
        self.pc += 1

        # Validate instruction format
        if len(line) < 6 or not line.isdigit():
            self.output_func(f"Invalid instruction: {line}")
            self.halted = True
            return

        # Parse instruction (3-digit opcode, 3-digit address)
        opcode = int(line[:3])
        address = int(line[3:6])

        if address < 0 or address >= 250:
            self.output_func(f"Invalid memory address: {address}")
            self.halted = True
            return

        # opcode execution
        if opcode == 10:        # read
            self.memory[address] = self.input_func("Enter value:")

        elif opcode == 11:      # write
            self.output_func(self.memory[address])

        elif opcode == 20:      # load
            self.acc = self.memory[address]

        elif opcode == 21:      # strore
            self.memory[address] = self.acc

        elif opcode == 30:      # add
            self.acc += self.memory[address]
            self.acc %= 1000000  # keep 6-digit limit

        elif opcode == 31:      # subtract
            self.acc -= self.memory[address]
            self.acc %= 1000000

        elif opcode == 32:      # divide
            if self.memory[address] == 0:
                self.output_func("Error: divide by zero")
                self.halted = True
            else:
                self.acc //= self.memory[address]

        elif opcode == 33:      # multiply
            self.acc *= self.memory[address]
            self.acc %= 1000000

        elif opcode == 40:      # branch
            self.pc = address

        elif opcode == 41:      # branchneg
            if self.acc < 0:
                self.pc = address

        elif opcode == 42:      # branchzero
            if self.acc == 0:
                self.pc = address

        elif opcode == 43:      # halt
            self.halted = True

        else:
            self.output_func(f"Unknown opcode: {opcode}")
            self.halted = True
