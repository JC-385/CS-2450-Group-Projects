import tkinter as tk
import os
import sys
from Simulator import BasicMLSimulator
root = tk.Tk()
root.title("Basic GUI")
root.geometry("400x400")

# Label - displays text
label = tk.Label(root, text="Hello, User!")
label.pack(pady=10)

# Entry - single-line input
entry = tk.Entry(root, width=25)
entry.pack(pady=5)

# Variable to signal when user has submitted (button clicked)
result_var = tk.StringVar()

def on_click():
    result_var.set(entry.get())

def clear_text(event):
    entry.delete(0, tk.END)
    entry.unbind("<FocusIn>")

def getEntryValue(entryType):
    entry.delete(0, tk.END)  # Clear first
    if entryType == "file":
        entry.insert(0, "Enter file name:")
    else:
        entry.insert(0, "Enter value:")

    entry.bind("<FocusIn>", clear_text)
    root.wait_variable(result_var)  # Blocks until result_var is set
    return result_var.get()

# Button - with a callback
button = tk.Button(root, text="RUN", command=on_click)
button.pack(pady=10)


def second_button():
    #this prints all the operations the program has
    operations = [ 'I/O operation:',
    'READ = 10 Read a word from the keyboard into a specific location in memory.',
    'WRITE = 11 Write a word from a specific location in memory to screen.',
    'Load/store operations:',
    'LOAD = 20 Load a word from a specific location in memory into the accumulator.',
    'STORE = 21 Store a word from the accumulator into a specific location in memory.',
    'Arithmetic operation:',
    'ADD = 30 Add a word from a specific location in memory to the word in the accumulator.',
    'SUBTRACT = 31 Subtract a word from a specific location in memory from the word in the accumulator.',
    'DIVIDE = 32 Divide the word in the accumulator by a word from a specific location in memory.',
    'MULTIPLY = 33 multiply a word from a specific location in memory to the word in the accumulator.',
    'Control operation:',
    'BRANCH = 40 Branch to a specific location in memory',
    'BRANCHNEG = 41 Branch to a specific location in memory if the accumulator is negative.',
    'BRANCHZERO = 42 Branch to a specific location in memory if the accumulator is zero.',
    'HALT = 43 Pause the program']
    print('Program operations')
    for i in operations:
        print(f'{i}\n')



button2 = tk.Button(root, text="Operation Instructions", command=second_button)
button2.pack(pady = 10)

def third_button():
    #this operation will close the app.
    root.destroy()

close_button = tk.Button(root, text="Exit Program", command=third_button)
close_button.pack(pady=10)


def reset_bt():
    root.destroy()
    os.execl(sys.executable, sys.executable, *sys.argv)

reset_button = tk.Button(root, text="Reset Program", command=reset_bt)
reset_button.pack(pady=10)


def run_gui():
    """Start the GUI event loop. Call this from Main when you want to show the window."""
    root.mainloop()