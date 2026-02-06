#I/O operation:
#READ = 10 Read a word from the keyboard into a specific location in memory.
from itertools import accumulate


def READ(location, memory):
    toStore = int(input("Enter a word: "))
    memory[int(location)] = toStore
    return memory
#WRITE = 11 Write a word from a specific location in memory to screen.
def WRITE(location, memory):
    print(memory[int(location)])
#Load/store operations:
#LOAD = 20 Load a word from a specific location in memory into the accumulator.
def LOAD(location, memory):
    return memory[int(location)]
#STORE = 21 Store a word from the accumulator into a specific location in memory.
def STORE(location, memory, accumulator):
    memory[int(location)] = accumulator 

#Arithmetic operation:
#ADD = 30 Add a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator)
def ADD(location, memory, accumulator):
    accumulator = accumulator + memory[int(location)]
    return accumulator;
#SUBTRACT = 31 Subtract a word from a specific location in memory from the word in the accumulator (leave the result in the accumulator)
def SUBTRACT(location, memory, accumulator):
    accumulator = accumulator - memory[int(location)]
    return accumulator;
#DIVIDE = 32 Divide the word in the accumulator by a word from a specific location in memory (leave the result in the accumulator).
def DIVIDE(location, memory, accumulator):
    accumulator = accumulator / memory[int(location)]
    return accumulator;
#MULTIPLY = 33 multiply a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator).
def MULTIPLY(location, memory, accumulator):
    accumulator = accumulator * memory[int(location)]
    return accumulator;

#Control operation:
#BRANCH = 40 Branch to a specific location in memory
#BRANCHNEG = 41 Branch to a specific location in memory if the accumulator is negative.
#BRANCHZERO = 42 Branch to a specific location in memory if the accumulator is zero.
#HALT = 43 Pause the program