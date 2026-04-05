"""UVSim graphical user interface.

Provides a tkinter-based GUI for the BasicML virtual machine simulator.
Allows users to browse and edit BasicML program files, run them with
interactive I/O, customize theme colors, and view operation reference.
"""

import tkinter as tk
import os
import sys
from tkinter import filedialog
from tkinter.filedialog import askopenfile, askopenfilename
from Simulator import BasicMLSimulator
import tkinter.font as tkFont

def load_theme():
    """Load custom theme colors from file.
    
    Reads theme.txt to load primary and secondary colors as hex codes.
    Falls back to default colors (UVU green and white) if file not found
    or parsing fails.
    
    Returns:
        dict: Theme dictionary with 'primary' and 'secondary' hex colors.
    """
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
    """Save custom theme colors to theme.txt file.
    
    Writes current theme color selections to theme.txt in format:
    primary=<hex_color>
    secondary=<hex_color>
    
    Colors are read from GUI input fields (primary_entry, secondary_entry).
    Updates status message and suggests restart to apply changes.
    """
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

# Tracks the currently open file path; used by save_file() to save to the same location
current_filepath = None

# Select best available monospace font for code display (in order of preference)
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
    """Execute a loaded BasicML program in console mode."""
    simulator = BasicMLSimulator(console_input, console_output)

    filename = filename_entry.get()
    simulator.load_program(filename)

    enter_console()

    simulator.run()
    
def clear_text(event):
    """Clear placeholder text from entry field on focus.
    
    Removes preview text when user clicks on the filename entry field,
    preparing it for actual input.
    
    Args:
        event: tkinter event object (unused).
    """
    filename_entry.delete(0, tk.END)
    filename_entry.unbind("<FocusIn>")

def open_file():
    """Open a file browser and load selected BasicML program into editor.
    
    Allows user to browse filesystem and select a .txt file containing
    BasicML instructions. Updates filename field with selected path and
    displays file contents in the text editor.
    """
    global current_filepath

    filepath = askopenfilename(filetypes =[("Text file", "*.txt"),("All Files", "*.*")])

    if filepath:
        current_filepath = filepath
        filename_entry.delete(0,tk.END)
        filename_entry.insert(0, filepath)
        with open(filepath, 'r') as file:
            text.delete('1.0', tk.END)
            text.insert(tk.END, file.read())

def save_file():
    """Save editor contents to file.
    
    Saves the current text editor contents back to the file. If no file
    has been opened, prompts user for a save location.
    """
    global current_filepath

    if current_filepath is None:
        current_filepath = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('Text Files', '*.txt')])

    if current_filepath:
        with open(current_filepath, 'w') as file:
            file.write(text.get('1.0', tk.END))

def console_instructions():
    """Display all 13 BasicML operations to console."""
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
    """Restart the UVSim application.
    
    Closes the current GUI window and relaunches the application from
    the entry point to reset all state.
    """
    root.destroy()
    os.execl(sys.executable, sys.executable, *sys.argv)

def close_application():
    """Close the UVSim application.
    
    Destroys the GUI window and exits the program.
    """
    root.destroy()

def enter_console():
    """Display console for program I/O and hide editor controls."""
    # Hide file editing and program listing widgets
    file_control_container.grid_forget()
    text.grid_forget()
    run_button.grid_forget()
    instructions_label.grid_forget()
    operation_instructions.grid_forget()
    application_control_container.grid_forget()

    # Display console
    console.grid(row=2, column=0, padx=20, pady=20, sticky='nsew')
    console.columnconfigure(0, weight=1)
    console.rowconfigure(0, weight=1)

    application_control_container.grid(row=6, column=0, padx=10, pady=10, sticky='ew')

def console_output(output):
    """Display a value in the console."""
    output_element = tk.Label(console, text=output)
    output_element.pack()

def console_input(prompt):
    """Prompt for user input during program execution.
    
    Args:
        prompt (str): Instructions to display above input field.
    
    Returns:
        str: The text entered by the user.
    """
    input_container = tk.Frame(console)
    input_container.pack(fill='x', pady=5)

    tk.Label(input_container, text=prompt).pack(side=tk.LEFT, anchor='w')

    input_field = tk.Entry(input_container)
    input_field.pack(side=tk.LEFT, fill='x')

    done = tk.BooleanVar(value=False)

    def submit():
        done.set(True)

    tk.Button(input_container, text="Submit", command=submit).pack(side=tk.LEFT)

    input_field.focus_set()

    root.update_idletasks()
    root.wait_variable(done)

    return input_field.get()

# Layout setup: use grid for all root children
root.columnconfigure(0, weight=1)
root.rowconfigure(2, weight=1)

label = tk.Label(root, text="Hello, User!", bg=theme["primary"], fg="white")
label.grid(row=0, column=0, pady=10, sticky='ew')

console = tk.Frame(root)

file_control_container = tk.Frame(root, bg=theme["secondary"])
file_control_container.grid(row=1, column=0, padx=10, pady=10, sticky='ew')
file_control_container.columnconfigure(0, weight=1)
file_control_container.columnconfigure(1, weight=0)
file_control_container.columnconfigure(2, weight=0)

filename_entry = tk.Entry(file_control_container, width=40)
filename_entry.grid(row=0, column=0, padx=5, sticky='ew')

# File action buttons
open_button = tk.Button(file_control_container, text="Open File", command=open_file,
                        bg=theme["primary"], fg="white")
open_button.grid(row=0, column=1, padx=5)
save_button = tk.Button(file_control_container, text="Save File", command=save_file,
                        bg=theme["primary"], fg="white")
save_button.grid(row=0, column=2, padx=5)

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
