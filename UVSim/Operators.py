class Operators:
    def READ(self, address, memory, input_function):
        memory[address] = int(input_function("Enter value: "))

    def WRITE(self, address, memory, output_function):
        output_function(memory[address])

    def LOAD(self, address, memory):
        return memory[address]

    def STORE(self, address, memory, accumulator):
        memory[address] = accumulator

    def ADD(self, address, memory, accumulator):
        return (accumulator + memory[address]) % 1000000  # keep 6-digit limit

    def SUBTRACT(self, address, memory, accumulator):
        return (accumulator - memory[address]) % 1000000  # keep 6-digit limit

    def DIVIDE(self, address, memory, accumulator):
        if memory[address] == 0:
            raise ZeroDivisionError("Error: divide by zero")
        return accumulator // memory[address]

    def MULTIPLY(self, address, memory, accumulator):
        return (accumulator * memory[address]) % 1000000  # keep 6-digit limit

    def BRANCH(self, address):
        return address

    def BRANCHNEG(self, address, accumulator):
        if accumulator < 0:
            return address
        return None

    def BRANCHZERO(self, address, accumulator):
        if accumulator == 0:
            return address
        return None

    def HALT(self):
        return True
