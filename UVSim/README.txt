UVSim - BasicML Virtual Machine Simulator

OVERVIEW
--------
UVSim is an educational virtual machine that interprets BasicML, a simple 
assembly-like machine language. It helps students understand low-level 
programming and computer architecture.

QUICK START
-----------
Requirements: Python 3.7+, tkinter (included with Python)

Run: python Main.py

Then use the GUI to:
- Open a .txt file with BasicML instructions
- Edit the program if needed
- Click "Run" to execute
- Enter inputs when prompted (terminal)
- View output in terminal

FILE FORMAT
-----------
Instructions are 4 digits per line: XXYY
  XX = Operation code (10-43)
  YY = Memory address (00-99)

Example:
  1000  (READ into address 0)
  2000  (LOAD address 0 to accumulator)
  3001  (ADD address 1)
  1100  (WRITE result)
  4300  (HALT)

MEMORY & MACHINE
----------------
- Memory: 250 words (addresses 0-249)
- Value range: -9999 to 9999
- Accumulator: Working register for arithmetic
- Program Counter: Instruction pointer (starts at 0)

OPERATIONS (13 total)
---------------------
I/O:          Control:
  10 READ       40 BRANCH
  11 WRITE      41 BRANCHNEG
              42 BRANCHZERO
Load/Store:     43 HALT
  20 LOAD
  21 STORE    Arithmetic:
              30 ADD
              31 SUBTRACT
              32 DIVIDE
              33 MULTIPLY

TESTING
-------
Run tests: pytest UVSim/test_operators.py

(23 tests covering all operations)

NOTES
-----
- Input validated: -9999 to 9999
- HALT (43) required to end program
- Theme colors customizable in GUI
- All I/O through terminal during execution