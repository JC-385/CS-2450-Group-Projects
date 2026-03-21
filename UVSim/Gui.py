import tkinter as tk
import os
import sys
from tkinter import filedialog
from tkinter.filedialog import askopenfile, askopenfilename
from Simulator import BasicMLSimulator
root = tk.Tk()
root.title("Basic GUI")
root.geometry("900x900")

# Label - displays text
label = tk.Label(root, text="Hello, User!")
label.pack(pady=10)

# Entry - single-line input
entry = tk.Entry(root, width=25)
entry.pack(pady=5)

# Variable to signal when user has submitted (button clicked)
result_var = tk.StringVar()
current_filepath = None

#this creates a small text editor where you can modify the text file with your operations
text = tk.Text(root, fg='dark green', bg='white', font='times-new-roman 14', width=50, height=10)
text.pack()

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

#this allows you to open your file that you want.
def open_file():
    global current_filepath

    filepath = askopenfilename(filetypes =[("Text file", "*.txt"),("All Files", "*.*")])

    if filepath:
        current_filepath = filepath
        entry.delete(0,tk.END)
        entry.insert(0, filepath)
        with open(filepath, 'r') as file:
            text.delete('1.0', tk.END)
            text.insert(tk.END, file.read())
#this saves the changes to your file.
def save_file():
    global current_filepath

    
    if current_filepath is None:
        current_filepath = filedialog.asksaveasfile(defaultextension='.txt', filetypes=[('Text Files', '*.txt')])

    if current_filepath:
        with open(current_filepath, 'w') as file:
            file.write(text.get('1.0', tk.END))

#Button - with a callback
tk.Button(root, text="Open File", command=open_file).pack(pady = 10)
tk.Button(root, text="Save File", command=save_file).pack(pady = 10)
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