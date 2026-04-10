import tkinter as tk
import os
import sys
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from tkinter.simpledialog import askstring
import tkinter.font as tkFont
from Simulator import BasicMLSimulator


# theme
def load_theme():
    default = {
        "primary": "#4C721D",
        "secondary": "#FFFFFF"
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

    status_label.config(text="Theme saved! Restart the app to apply.")


theme = load_theme()


#root window
root = tk.Tk()
root.title("UVSim")
root.geometry("900x900")
root.configure(bg=theme["secondary"])

result_var = tk.StringVar()
current_filepath = None


#font selection
preferred_fonts = ["Menlo", "Consolas", "DejaVu Sans Mono", "Courier New", "Courier"]
available_fonts = tkFont.families()
mono_font = next((f for f in preferred_fonts if f in available_fonts), "TkFixedFont")


#instruction reference
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


#console I/O functions
def console_output(output):
    text.insert(tk.END, str(output) + "\n")
    text.see(tk.END)
    root.update_idletasks()


def console_input(prompt):
    value = askstring("Input Required", prompt)
    if value is None or value.strip() == "":
        value = "0"
    return int(value)


# Global simulator instance
simulator = None


# helper: check line count limit
def exceeds_line_limit(content):
    return len(content.strip().split("\n")) > 250


#run program 
def run_program():
    global simulator

    text.delete("1.0", tk.END)

    filename = filename_entry.get()
    if not filename:
        status_label.config(text="Enter file name first.")
        return

    try:
        with open(filename, "r") as f:
            lines = f.readlines()
            if len(lines) > 250:
                status_label.config(text="ERROR: Program exceeds 250 lines.")
                return
    except FileNotFoundError:
        status_label.config(text=f"File not found: {filename}")
        return

    simulator = BasicMLSimulator(console_input, console_output)

    try:
        simulator.load_program(filename)
    except Exception as e:
        status_label.config(text=f"ERROR: {e}")
        return

    status_label.config(text=f"Running: {filename}")

    # stepping function
    def step_sim():
        if simulator and not simulator.halted and simulator.pc < len(simulator.program):
            simulator.step()
            root.after(10, step_sim)
        else:
            status_label.config(text=f"Finished: {filename}")

    step_sim()


#open/save file functions
def open_file():
    global current_filepath

    filepath = askopenfilename(filetypes=[("Text file", "*.txt"), ("All Files", "*.*")])

    if filepath:
        with open(filepath, "r") as file:
            content = file.read()

        if exceeds_line_limit(content):
            status_label.config(text="ERROR: File exceeds 250 lines.")
            return

        current_filepath = filepath
        filename_entry.delete(0, tk.END)
        filename_entry.insert(0, filepath)

        text.delete("1.0", tk.END)
        text.insert(tk.END, content)


def save_file():
    global current_filepath

    content = text.get("1.0", tk.END)

    if exceeds_line_limit(content):
        status_label.config(text="ERROR: Cannot save more than 250 lines.")
        return

    if current_filepath is None:
        current_filepath = filedialog.asksaveasfilename(defaultextension='.txt',
                                                        filetypes=[('Text Files', '*.txt')])

    if current_filepath:
        with open(current_filepath, "w") as file:
            file.write(content)


#window control functions
def reset_application():
    root.destroy()
    os.execl(sys.executable, sys.executable, *sys.argv)


def close_application():
    root.destroy()


#layout configuration
root.columnconfigure(0, weight=1)
root.rowconfigure(2, weight=1)

label = tk.Label(root, text="Hello, User!", bg=theme["primary"], fg="white")
label.grid(row=0, column=0, pady=10, sticky='ew')

# FILE BAR
file_control_container = tk.Frame(root, bg=theme["secondary"])
file_control_container.grid(row=1, column=0, padx=10, pady=10, sticky='ew')
file_control_container.columnconfigure(0, weight=1)

filename_entry = tk.Entry(file_control_container, width=40)
filename_entry.grid(row=0, column=0, padx=5, sticky='ew')

open_button = tk.Button(file_control_container, text="Open File", command=open_file,
                        bg=theme["primary"], fg="white")
open_button.grid(row=0, column=1, padx=5)

save_button = tk.Button(file_control_container, text="Save File", command=save_file,
                        bg=theme["primary"], fg="white")
save_button.grid(row=0, column=2, padx=5)

# text editor
text = tk.Text(root, fg="dark green", bg=theme["secondary"], font=(mono_font, 14),
               bd=2, highlightthickness=2, highlightbackground="#000", height=20)
text.grid(row=2, column=0, padx=20, pady=20, sticky='nsew')

run_button = tk.Button(root, text="RUN", command=run_program,
                       bg=theme["primary"], fg="white")
run_button.grid(row=3, column=0, pady=10)

# instructions
instructions_label = tk.Label(root, text="List of Functions:", anchor="center")
instructions_label.grid(row=4, column=0, sticky='ew', padx=10)

operation_instructions = tk.Message(root, text=instructions, width=1000,
                                    font=(mono_font, 12), bg=theme["secondary"])
operation_instructions.grid(row=5, column=0, padx=10, sticky='ew')

# bottom control bar
application_control_container = tk.Frame(root, bg=theme["secondary"])
application_control_container.grid(row=6, column=0, padx=10, pady=10, sticky='ew')

reset_button = tk.Button(application_control_container, text="Reset Program",
                         command=reset_application, width=30,
                         bg=theme["primary"], fg="white")
reset_button.grid(row=0, column=0, padx=10)

close_button = tk.Button(application_control_container, text="Exit Program",
                         command=close_application, width=30,
                         bg=theme["primary"], fg="white")
close_button.grid(row=0, column=1, padx=10)

# theme editor
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
                              command=save_theme, bg=theme["primary"], fg="white")
save_theme_button.grid(row=2, column=0, columnspan=2, pady=10)

status_label = tk.Label(theme_frame, text="", bg=theme["secondary"])
status_label.grid(row=3, column=0, columnspan=2)


#publish function
def run_gui():
    root.mainloop()


def focus_window():
    root.lift()
    root.focus_force()


root.after(0, focus_window)
