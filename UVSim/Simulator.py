from operators import Operators   

class BasicMLSimulator:
    def __init__(self, input_function, output_function):
        self.memory = [0] * 250   # 250 memory slots
        self.accumulator = 0
        self.pc = 0                 # program counter
        self.halted = False
        self.program = []
        self.word_size = 4          # track 4-digit or 6-digit format

        self.op = Operators()       # operation handler

        self.input_function = input_function
        self.output_function = output_function

    def load_program(self, filename):
        """Load file into self.program list."""
        with open(filename, "r") as file:
            lines = [line.strip() for line in file if line.strip()]

        # enforce max 250 lines
        if len(lines) > 250:
            raise ValueError("Program exceeds 250 lines")

        # detect format (4-digit or 6-digit)
        if all(len(line) == 4 for line in lines):
            self.word_size = 4
        elif all(len(line) == 6 for line in lines):
            self.word_size = 6
        else:
            raise ValueError("Mixed or invalid instruction format")

        self.program = lines
        self.pc = 0
        self.halted = False

    def step(self):
        """Execute a single instruction."""
        if self.pc >= len(self.program) or self.halted:
            return

        line = self.program[self.pc]

        # Program counter always increments unless a branch occurs
        self.pc += 1

        # Validate instruction format
        if not line.isdigit():
            self.output_function(f"Invalid instruction: {line}")
            self.halted = True
            return

        # parsing based on format
        if len(line) == 4:
            opcode = int(line[:2])
            address = int(line[2:])
        elif len(line) == 6:
            opcode = int(line[1:3])   # skip leading 0 → FIX
            address = int(line[3:])
        else:
            self.output_function(f"Invalid instruction length: {line}")
            self.halted = True
            return

        # normalize opcode (remove leading zero if needed)
        if self.word_size == 6:
            opcode = int(str(opcode).lstrip("0"))

        # Validate memory address
        if address < 0 or address > 249:
            self.output_function(f"Invalid memory address: {address}")
            self.halted = True
            return

        # opcode execution
        try:
            if opcode == 10:        # read
                self.memory[address] = int(self.input_function("Enter value:"))

            elif opcode == 11:      # write
                self.output_function(self.memory[address])

            elif opcode == 20:      # load
                self.accumulator = self.memory[address]

            elif opcode == 21:      # store
                self.memory[address] = self.accumulator

            elif opcode == 30:      # add
                self.accumulator += self.memory[address]
                self.accumulator %= 1000000  # keep 6-digit limit

            elif opcode == 31:      # subtract
                self.accumulator -= self.memory[address]
                self.accumulator %= 1000000

            elif opcode == 32:      # divide
                if self.memory[address] == 0:
                    self.output_function("Error: divide by zero")
                    self.halted = True
                    return
                self.accumulator //= self.memory[address]

            elif opcode == 33:      # multiply
                self.accumulator *= self.memory[address]
                self.accumulator %= 1000000

            elif opcode == 40:      # branch
                self.pc = address

            elif opcode == 41:      # branchneg
                if self.accumulator < 0:
                    self.pc = address

            elif opcode == 42:      # branchzero
                if self.accumulator == 0:
                    self.pc = address

            elif opcode == 43:      # halt
                self.halted = True

            else:
                self.output_function(f"Unknown opcode: {opcode}")
                self.halted = True

        except Exception as e:
            self.output_function(f"Runtime error: {e}")
            self.halted = True

    def run(self):
        while not self.halted and self.pc < len(self.program):
            self.step()

    def print_memory(self):
        print(self.memory)

    def reset(self):
        self.memory = [0] * 250   # UPDATED
        self.accumulator = 0
        self.pc = 0
        self.halted = False
        self.program = []
