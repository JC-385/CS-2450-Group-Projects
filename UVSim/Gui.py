import tkinter as tk
import os
import sys
from tkinter import filedialog
from tkinter.filedialog import askopenfile, askopenfilename
from Simulator import BasicMLSimulator
root = tk.Tk()
root.title("UVSim")
root.geometry("900x900")

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

def close():
    # closes the app
    root.destroy()

def reset_bt():
    root.destroy()
    os.execl(sys.executable, sys.executable, *sys.argv)

# Label - displays text
label = tk.Label(root, text="Hello, User!")
label.pack(pady=10)

# File control - top row of file-control related elements
file_control_container = tk.Frame(root)
file_control_container.pack(pady=10)

# Filename entry - single-line input
filename_entry = tk.Entry(file_control_container, width=40)
filename_entry.pack(side=tk.LEFT, padx=5)

# File action buttons inside file control container
open_button = tk.Button(file_control_container, text="Open File", command=open_file)
open_button.pack(side=tk.LEFT, padx=5)
save_button = tk.Button(file_control_container, text="Save File", command=save_file)
save_button.pack(side=tk.LEFT, padx=5)

# Variable to signal when user has submitted (button clicked)
result_var = tk.StringVar()
current_filepath = None

# Small text editor where you can modify the text file with your operations
text = tk.Text(root, fg='dark green', bg='white', font='times-new-roman 14', width=50, height=10)
text.pack()

run_button = tk.Button(root, text="RUN", command=run_program)
run_button.pack(pady=10)

operation_instructions = tk.Button(root, text="Operation Instructions", command=console_instructions)
operation_instructions.pack(pady = 10)

close_button = tk.Button(root, text="Exit Program", command=close)
close_button.pack(pady=10)

reset_button = tk.Button(root, text="Reset Program", command=reset_bt)
reset_button.pack(pady=10)

def run_gui():
    """Start the GUI event loop. Call this from Main when you want to show the window."""
    root.mainloop()