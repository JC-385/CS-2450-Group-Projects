import tkinter as tk
import os
import sys
from tkinter import filedialog
from tkinter.filedialog import askopenfile, askopenfilename
from Simulator import BasicMLSimulator
import tkinter.font as tkFont
root = tk.Tk()
root.title("UVSim")
# root.geometry("900x900")

# Variable to signal when user has submitted (button clicked)
result_var = tk.StringVar()
current_filepath = None

preferred_fonts = ["Menlo", "Consolas", "DejaVu Sans Mono", "Courier New", "Courier"]
available_fonts = tkFont.families()
mono_font = next((f for f in preferred_fonts if f in available_fonts), "TkFixedFont")

instructions = """I/O         READ = 10 Read a word from the keyboard into a specific location in memory.
            WRITE = 11 Write a word from a specific location in memory to screen.
Load/store  LOAD = 20 Load a word from a specific location in memory into the accumulator.
            STORE = 21 Store a word from the accumulator into a specific location in memory.
Arithmetic  ADD = 30 Add a word from a specific location in memory to the word in the accumulator.
            SUBTRACT = 31 Subtract a word from a specific location in memory from the word in the accumulator.
            DIVIDE = 32 Divide the word in the accumulator by a word from a specific location in memory.
            MULTIPLY = 33 multiply a word from a specific location in memory to the word in the accumulator.
Control     BRANCH = 40 Branch to a specific location in memory
            BRANCHNEG = 41 Branch to a specific location in memory if the accumulator is negative.
            BRANCHZERO = 42 Branch to a specific location in memory if the accumulator is zero.
            HALT = 43 Pause the program"""

def run_program():
    result_var.set(filename_entry.get())

def clear_text(event):
    filename_entry.delete(0, tk.END)
    filename_entry.unbind("<FocusIn>")

def getEntryValue(entryType):
    filename_entry.delete(0, tk.END)  # Clear first
    if entryType == "file":
        filename_entry.insert(0, "Enter file name:")
    else:
        filename_entry.insert(0, "Enter value:")

    filename_entry.bind("<FocusIn>", clear_text)
    root.wait_variable(result_var)  # Blocks until result_var is set
    return result_var.get()

# allows you to open the file that you want
def open_file():
    global current_filepath

    filepath = askopenfilename(filetypes =[("Text file", "*.txt"),("All Files", "*.*")])

    if filepath:
        current_filepath = filepath
        filename_entry.delete(0,tk.END)
        filename_entry.insert(0, filepath)
        with open(filepath, 'r') as file:
            text.delete('1.0', tk.END)
            text.insert(tk.END, file.read())

# saves the changes to your file
def save_file():
    global current_filepath

    if current_filepath is None:
        current_filepath = filedialog.asksaveasfile(defaultextension='.txt', filetypes=[('Text Files', '*.txt')])

    if current_filepath:
        with open(current_filepath, 'w') as file:
            file.write(text.get('1.0', tk.END))

def console_instructions():
    # prints all the operations the program has
    operations = [
        'Program operations:',
        'I/O operation:',
        '   READ = 10 Read a word from the keyboard into a specific location in memory.',
        '   WRITE = 11 Write a word from a specific location in memory to screen.',
        '   Load/store operations:',
        '   LOAD = 20 Load a word from a specific location in memory into the accumulator.',
        '   STORE = 21 Store a word from the accumulator into a specific location in memory.',
        'Arithmetic operation:',
        '   ADD = 30 Add a word from a specific location in memory to the word in the accumulator.',
        '   SUBTRACT = 31 Subtract a word from a specific location in memory from the word in the accumulator.',
        '   DIVIDE = 32 Divide the word in the accumulator by a word from a specific location in memory.',
        '   MULTIPLY = 33 multiply a word from a specific location in memory to the word in the accumulator.',
        'Control operation:',
        '   BRANCH = 40 Branch to a specific location in memory',
        '   BRANCHNEG = 41 Branch to a specific location in memory if the accumulator is negative.',
        '   BRANCHZERO = 42 Branch to a specific location in memory if the accumulator is zero.',
        '   HALT = 43 Pause the program'
    ]
    print(*operations, sep="\n\n")

def reset_application():
    root.destroy()
    os.execl(sys.executable, sys.executable, *sys.argv)

def close_application():
    # closes the app
    root.destroy()

# Label - displays text
label = tk.Label(root, text="Hello, User!")
label.pack(pady=10)

# File control - top row of file control related elements
file_control_container = tk.Frame(root)
file_control_container.pack(padx=10, pady=10)

# Filename entry - single-line input
filename_entry = tk.Entry(file_control_container, width=40)
filename_entry.pack(side=tk.LEFT, padx=5)

# File action buttons inside file control container
open_button = tk.Button(file_control_container, text="Open File", command=open_file)
open_button.pack(side=tk.LEFT, padx=5)
save_button = tk.Button(file_control_container, text="Save File", command=save_file)
save_button.pack(side=tk.LEFT, padx=5)

# Small text editor where you can modify the text file with your operations
text = tk.Text(root, fg='dark green', bg='white', font=(mono_font, 14), height=10)
text.pack(fill='x')

run_button = tk.Button(root, text="RUN", command=run_program)
run_button.pack(pady=10)

# Removed button that sends instructions to console
# operation_instructions_button = tk.Button(root, text="Operation Instructions", command=console_instructions)
# operation_instructions_button.pack(pady = 10)

# Instructions for use
operation_instructions = tk.Message(root, text=instructions, width=1000, font=(mono_font, 12))
operation_instructions.pack(fill='x')

# Application control - bottom row of application control related elements
application_control_container = tk.Frame(root)
application_control_container.pack(padx=10)

# Application control buttons
reset_button = tk.Button(application_control_container, text="Reset Program", command=reset_application, width=30)
reset_button.pack(side=tk.LEFT, padx=5)
close_button = tk.Button(application_control_container, text="Exit Program", command=close_application, width=30)
close_button.pack(side=tk.LEFT, padx=5)

def run_gui():
    """Start the GUI event loop. Call this from Main when you want to show the window."""
    root.mainloop()

def focus_window():
    root.lift()
    root.focus_force()

root.after(0, focus_window)