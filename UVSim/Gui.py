import tkinter as tk
import os
import sys
from tkinter import filedialog
from tkinter.filedialog import askopenfile, askopenfilename
from Simulator import BasicMLSimulator
import tkinter.font as tkFont

# theme 
def load_theme():
    default = {
        "primary": "#4C721D",   # UVU green
        "secondary": "#FFFFFF" # white
    }

    try:
        with open("theme.txt", "r") as file:
            for line in file:
                key, value = line.strip().split("=")
                default[key.strip()] = value.strip()
    except:
        pass

    return default

def save_theme():
    primary = primary_entry.get()
    secondary = secondary_entry.get()

    with open("theme.txt", "w") as file:
        file.write(f"primary={primary}\n")
        file.write(f"secondary={secondary}\n")

    status_label.config(text="Theme saved! Restart app to apply.")

theme = load_theme()

root = tk.Tk()
root.title("UVSim")
root.geometry("900x900")
root.configure(bg=theme["secondary"])

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
    simulator = BasicMLSimulator(console_input, console_output)

    filename = filename_entry.get()
    simulator.load_program(filename)

    enter_console()

    simulator.run()
    
    # result_var.set(filename_entry.get())

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
        current_filepath = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('Text Files', '*.txt')])

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

def enter_console():
    file_control_container.grid_forget()
    text.grid_forget()
    run_button.grid_forget()
    instructions_label.grid_forget()
    operation_instructions.grid_forget()
    application_control_container.grid_forget()

    console.grid(row=2, column=0, padx=20, pady=20, sticky='nsew')
    console.columnconfigure(0, weight=1)
    console.rowconfigure(0, weight=1)

    application_control_container.grid(row=6, column=0, padx=10, pady=10, sticky='ew')

def console_output(output):
    output_element = tk.Label(console, text=output)
    output_element.pack()

def console_input(prompt):
    input_container = tk.Frame(console)
    input_container.pack(fill='x', pady=5)

    tk.Label(input_container, text=prompt).pack(anchor='w')

    input_field = tk.Entry(input_container)
    input_field.pack(fill='x')

    done = tk.BooleanVar(value=False)

    def submit():
        done.set(True)

    tk.Button(input_container, text="Submit", command=submit).pack()

    input_field.focus_set()

    root.update_idletasks()
    root.wait_variable(done)

    return input_field.get()

# Layout setup: use grid for all root children
root.columnconfigure(0, weight=1)
root.rowconfigure(2, weight=1)

# Label - displays text
label = tk.Label(root, text="Hello, User!", bg=theme["primary"], fg="white")
label.grid(row=0, column=0, pady=10, sticky='ew')

# Console - later added by enter_console()
console = tk.Frame(root)

# File control - top row of file control related elements
file_control_container = tk.Frame(root, bg=theme["secondary"])
file_control_container.grid(row=1, column=0, padx=10, pady=10, sticky='ew')
file_control_container.columnconfigure(0, weight=1)
file_control_container.columnconfigure(1, weight=0)
file_control_container.columnconfigure(2, weight=0)

# Filename entry - single-line input
filename_entry = tk.Entry(file_control_container, width=40)
filename_entry.grid(row=0, column=0, padx=5, sticky='ew')

# File action buttons inside file control container
open_button = tk.Button(file_control_container, text="Open File", command=open_file,
                        bg=theme["primary"], fg="white")
open_button.grid(row=0, column=1, padx=5)
save_button = tk.Button(file_control_container, text="Save File", command=save_file,
                        bg=theme["primary"], fg="white")
save_button.grid(row=0, column=2, padx=5)

# Small text editor where you can modify the text file with your operations
text = tk.Text(root, fg='dark green', bg=theme["secondary"], font=(mono_font, 14), bd=2, highlightthickness=2, highlightbackground="#000", height=20)
text.grid(row=2, column=0, padx=20, pady=20, sticky='nsew')

run_button = tk.Button(root, text="RUN", command=run_program,
                       bg=theme["primary"], fg="white")
run_button.grid(row=3, column=0, pady=10)

# Instructions
instructions_label = tk.Label(root, text="List of Functions:", anchor="center", justify="center")
instructions_label.grid(row=4, column=0, sticky='ew', padx=10)
operation_instructions = tk.Message(root, text=instructions, width=1000, font=(mono_font, 12),
                                     bg=theme["secondary"])
operation_instructions.grid(row=5, column=0, padx=10, sticky='ew')

# Application control - bottom row of application control related elements
application_control_container = tk.Frame(root, bg=theme["secondary"])
application_control_container.grid(row=6, column=0, padx=10, pady=10, sticky='ew')
application_control_container.columnconfigure(0, weight=1)
application_control_container.columnconfigure(1, weight=0)
application_control_container.columnconfigure(2, weight=1)
application_control_container.columnconfigure(3, weight=0)
application_control_container.columnconfigure(4, weight=1)

# Application control buttons
reset_button = tk.Button(application_control_container, text="Reset Program", command=reset_application, width=30,
                         bg=theme["primary"], fg="white")
reset_button.grid(row=0, column=1, sticky='e')
close_button = tk.Button(application_control_container, text="Exit Program", command=close_application, width=30,
                         bg=theme["primary"], fg="white")
close_button.grid(row=0, column=3, sticky='w')

# theme control
theme_frame = tk.Frame(root, bg=theme["secondary"])
theme_frame.grid(row=7, column=0, pady=20)

tk.Label(theme_frame, text="Primary Color (#HEX):", bg=theme["secondary"]).grid(row=0, column=0)
primary_entry = tk.Entry(theme_frame)
primary_entry.insert(0, theme["primary"])
primary_entry.grid(row=0, column=1)

tk.Label(theme_frame, text="Secondary Color (#HEX):", bg=theme["secondary"]).grid(row=1, column=0)
secondary_entry = tk.Entry(theme_frame)
secondary_entry.insert(0, theme["secondary"])
secondary_entry.grid(row=1, column=1)

save_theme_button = tk.Button(theme_frame, text="Save Theme",
                              command=save_theme,
                              bg=theme["primary"], fg="white")
save_theme_button.grid(row=2, column=0, columnspan=2, pady=10)

status_label = tk.Label(theme_frame, text="", bg=theme["secondary"])
status_label.grid(row=3, column=0, columnspan=2)

def run_gui():
    """Start the GUI event loop. Call this from Main when you want to show the window."""
    root.mainloop()

def focus_window():
    root.lift()
    root.focus_force()

root.after(0, focus_window)
