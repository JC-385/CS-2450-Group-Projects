"""BasicML virtual machine simulator.

Provides the core execution engine for BasicML programs. Implements the
fetch-decode-execute cycle with 250-byte memory, accumulator register,
program counter, and support for 13 operations.
"""

from Operators import *


class BasicMLSimulator:
    """Virtual machine for executing BasicML programs.
    
    Manages program execution cycle, memory, registers (accumulator, PC),
    and delegates operation execution to the Operators class.
    
    Attributes:
        memory (list): 250-element array of integers (0 initialized).
        accumulator (int): Working register for arithmetic results.
        pc (int): Program counter; index of next instruction to execute.
        halted (bool): Execution state flag; True when HALT encountered.
        program (list): Loaded list of instruction strings.
        op (Operators): Instance of Operators for executing instructions.
        input_function (callable): Callback for READ operation input.
        output_function (callable): Callback for WRITE operation output.
    """

    def __init__(self, input_function, output_function):
        """Initialize BasicML simulator with I/O callbacks.
        
        Args:
            input_function: Callback for READ operations.
                Signature: input_function(prompt: str) -> int
            output_function: Callback for WRITE operations.
                Signature: output_function(value: int) -> None
        """
        self.memory = [0] * 250
        self.accumulator = 0
        self.pc = 0
        self.halted = False
        self.program = []
        self.op = Operators()
        self.input_function = input_function
        self.output_function = output_function

    def load_program(self, filename):
        """Load a BasicML program from a text file.
        
        Reads the file and stores each line as an instruction. Each line
        should contain a 4-digit instruction code.
        
        Args:
            filename (str): Path to the program file.
        
        Raises:
            FileNotFoundError: If file does not exist.
            IndexError: If program has too many operations (>250).
        """
        with open(filename, "r") as file:
            lines = [line.strip() for line in file]
        if len(lines) > 250:
            raise IndexError("Too many operations.")
        self.program = lines

    def step(self):
        """Execute one instruction (fetch-decode-execute cycle).
        
        Fetches the instruction at program counter (pc), decodes the opcode
        and operand, executes the operation via Operators, and updates
        machine state. Stops if halted or at end of program.
        
        The instruction format is XXYY where XX is the opcode (10-43) and
        YY is the memory address operand.
        
        Raises:
            ValueError: If operation execution fails (e.g., invalid input).
            IndexError: If memory address is out of range.
        """
        if self.pc >= len(self.program) or self.halted:
            return
        line = self.program[self.pc]
        # Parse instruction: position 0 ignored, positions 1-2 are opcode, 3-4 are address
        if len(line) == 5:
            opcode = line[1:3]
            address = int(line[3:5])
        elif len(line) == 7:
            # Alternative format with different padding
            opcode = line[1:4]
            address = int(line[4:7])
        else:
            # Invalid format, skip this instruction
            print("Invalid operator")
            self.pc += 1
            return

        match opcode:
            case "10":
                self.op.READ(address, self.memory, self.input_function)
            case "11":
                self.op.WRITE(address, self.memory, self.output_function)
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
        """Execute program until HALT or end of program.
        
        Repeatedly calls step() to execute instructions sequentially until
        the halted flag is set (by HALT operation) or the program counter
        reaches the end of the program.
        """
        while not self.halted and self.pc < len(self.program):
            self.step()

    def print_memory(self):
        """Debug utility: Print entire memory contents.
        
        Outputs the current state of all 250 memory cells to the console.
        """
        print(self.memory)

    def reset(self):
        """Reset simulator to initial state.
        
        Clears memory, accumulator, program counter, halted flag, and
        program storage. Prepares simulator for loading and executing
        a new program.
        """
        self.memory = [0] * 100
        self.accumulator = 0
        self.pc = 0
        self.halted = False
        self.program = []