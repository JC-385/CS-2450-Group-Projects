"""BasicML operation implementations.

Provides all 13 operations supported by BasicML, organized by category:
- I/O: READ, WRITE
- Load/Store: LOAD, STORE
- Arithmetic: ADD, SUBTRACT, DIVIDE, MULTIPLY
- Control: BRANCH, BRANCHNEG, BRANCHZERO, HALT
"""


class Operators:
    """Implements all 13 BasicML operations.
    
    Each method represents one operation in the BasicML instruction set.
    Operations modify memory, accumulator, or return control flow changes
    based on the instruction semantics.
    """

    # I/O Operations

    def READ(self, location, memory, input_function):
        """Read an integer from input into memory.
        
        Prompts user to enter an integer, validates it is in range
        -9999 to 9999, and stores it at the specified memory address.
        
        Args:
            location: Memory address (0-249) to store input.
            memory: Memory array to modify.
            input_function: Callback to get user input.
                Signature: input_function(prompt: str) -> int
        
        Returns:
            Modified memory array.
        
        Raises:
            ValueError: If input is outside -9999 to 9999 range.
        """
        toStore = int(input_function("Enter a word"))
        if -9999 <= toStore <= 9999:
            memory[int(location)] = toStore
            return memory
        else:
            raise ValueError("Input must be between, -9999 and 9999.")

    def WRITE(self, location, memory, output_function):
        """Output a value from memory to the screen.
        
        Fetches the value at the specified memory address and sends it
        to output via the output callback.
        
        Args:
            location: Memory address (0-249) to read from.
            memory: Memory array to read from.
            output_function: Callback to output value.
                Signature: output_function(value: int) -> None
        """
        output_function(memory[int(location)])

    # Load/Store Operations

    def LOAD(self, location, memory):
        """Load a value from memory into the accumulator.
        
        Args:
            location: Memory address (0-249) to fetch from.
            memory: Memory array to read from.
        
        Returns:
            Value at memory[location].
        """
        return memory[int(location)]

    def STORE(self, location, memory, accumulator):
        """Store the accumulator value into memory.
        
        Args:
            location: Memory address (0-249) to store into.
            memory: Memory array to modify.
            accumulator: Value to store.
        """
        memory[int(location)] = accumulator 

    # Arithmetic Operations

    def ADD(self, location, memory, accumulator):
        """Add a memory value to the accumulator.
        
        Args:
            location: Memory address (0-249) to fetch from.
            memory: Memory array to read from.
            accumulator: Current accumulator value.
        
        Returns:
            Updated accumulator (accumulator + memory[location]).
        """
        accumulator = accumulator + memory[int(location)]
        return accumulator
    
    def SUBTRACT(self, location, memory, accumulator):
        """Subtract a memory value from the accumulator.
        
        Args:
            location: Memory address (0-249) to fetch from.
            memory: Memory array to read from.
            accumulator: Current accumulator value.
        
        Returns:
            Updated accumulator (accumulator - memory[location]).
        """
        accumulator = accumulator - memory[int(location)]
        return accumulator
    
    def DIVIDE(self, location, memory, accumulator):
        """Divide accumulator by a memory value (integer division).
        
        Performs integer division (// operator) to avoid floating-point
        results. Truncates toward negative infinity.
        
        Args:
            location: Memory address (0-249) to fetch from.
            memory: Memory array to read from.
            accumulator: Current accumulator value (dividend).
        
        Returns:
            Updated accumulator (accumulator // memory[location]).
        
        Raises:
            ZeroDivisionError: If memory[location] is zero.
        """
        accumulator = accumulator // memory[int(location)]
        return accumulator
    
    def MULTIPLY(self, location, memory, accumulator):
        """Multiply accumulator by a memory value.
        
        Args:
            location: Memory address (0-249) to fetch from.
            memory: Memory array to read from.
            accumulator: Current accumulator value.
        
        Returns:
            Updated accumulator (accumulator * memory[location]).
        """
        accumulator = accumulator * memory[int(location)]
        return accumulator

    # Control Operations
    
    def BRANCH(self, location):
        """Unconditionally jump to an instruction at specified address.
        
        Args:
            location: Target memory address (0-249) to branch to.
        
        Returns:
            The target address for program counter to jump to.
        """
        return int(location)
    
    def BRANCHNEG(self, address, accumulator):
        """Conditionally jump if accumulator is negative.
        
        Tests the accumulator value. If negative, returns target address
        for branch. Otherwise returns None to indicate branch not taken.
        
        Args:
            address: Target memory address (0-249) to branch to.
            accumulator: Current accumulator value to test.
        
        Returns:
            int: Target address if accumulator < 0, else None.
        """
        if accumulator < 0:
            return int(address)
        return None
    
    def BRANCHZERO(self, address, accumulator):
        """Conditionally jump if accumulator is zero.
        
        Tests the accumulator value. If zero, returns target address for
        branch. Otherwise returns None to indicate branch not taken.
        
        Args:
            address: Target memory address (0-249) to branch to.
            accumulator: Current accumulator value to test.
        
        Returns:
            int: Target address if accumulator == 0, else None.
        """
        if accumulator == 0:
            return int(address)
        return None
    
    def HALT(self):
        """Signal end of program execution.
        
        Sets the halted flag to stop the fetch-decode-execute loop.
        
        Returns:
            True to indicate halt state.
        """
        return True