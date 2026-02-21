import tkinter as tk

root = tk.Tk()
root.title("Basic GUI")
root.geometry("300x200")

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

def getEntryValue(entryType):
    entry.delete(0, tk.END)  # Clear first
    if entryType == "file":
        entry.insert(0, "Enter file name:")
    else:
        entry.insert(0, "Enter value:")
    root.wait_variable(result_var)  # Blocks until result_var is set
    return result_var.get()

# Button - with a callback
button = tk.Button(root, text="Click Me", command=on_click)
button.pack(pady=10)

def run_gui():
    """Start the GUI event loop. Call this from Main when you want to show the window."""
    root.mainloop()