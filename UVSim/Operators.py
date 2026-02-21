class Operators:
    #I/O operation:
    #READ = 10 Read a word from the keyboard into a specific location in memory.

    def READ(self, location, memory):
        toStore = int(input("Enter a word: "))
        if -9999 <= toStore <= 9999:
            memory[int(location)] = toStore
            return memory
        else:
            raise ValueError("Input must be between, -9999 and 9999.")
    #WRITE = 11 Write a word from a specific location in memory to screen.
    def WRITE(self, location, memory):
        print(memory[int(location)])
    #Load/store operations:
    #LOAD = 20 Load a word from a specific location in memory into the accumulator.
    def LOAD(self, location, memory):
        return memory[int(location)]
    #STORE = 21 Store a word from the accumulator into a specific location in memory.
    def STORE(self, location, memory, accumulator):
        memory[int(location)] = accumulator 

    #Arithmetic operation:
    #ADD = 30 Add a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator)
    def ADD(self, location, memory, accumulator):
        accumulator = accumulator + memory[int(location)]
        return accumulator;
    #SUBTRACT = 31 Subtract a word from a specific location in memory from the word in the accumulator (leave the result in the accumulator)
    def SUBTRACT(self, location, memory, accumulator):
        accumulator = accumulator - memory[int(location)]
        return accumulator;
    #DIVIDE = 32 Divide the word in the accumulator by a word from a specific location in memory (leave the result in the accumulator).
    def DIVIDE(self, location, memory, accumulator):
        accumulator = accumulator // memory[int(location)]
        return accumulator;
    #MULTIPLY = 33 multiply a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator).
    def MULTIPLY(self, location, memory, accumulator):
        accumulator = accumulator * memory[int(location)]
        return accumulator;

    #Control operation:
    #BRANCH = 40 Branch to a specific location in memory
    def BRANCH(self, location):
        return int(location)
    #BRANCHNEG = 41 Branch to a specific location in memory if the accumulator is negative.
    def BRANCHNEG(self, address, accumulator):
        if accumulator < 0:
            return int(address)
        return None
    #BRANCHZERO = 42 Branch to a specific location in memory if the accumulator is zero.
    def BRANCHZERO(self, address, accumulator):
        if accumulator == 0:
            return int(address)
        return None
    #HALT = 43 Pause the program
    def HALT(self):
        return True