import tkinter as tk
import subprocess

def run_virtual_keyboard():
    subprocess.Popen(['python', 'virtualkey.py'])

def run_paint():
    subprocess.Popen(['python', 'paint1.py'])

# Create main window
root = tk.Tk()
root.title("Hand Gesture Project")
root.geometry("400x200")
root.configure(bg="#f0f0f0")

# Title label
title_label = tk.Label(root, text="Hand Gesture Project", font=("Arial", 20, "bold"), bg="#f0f0f0")
title_label.pack(pady=20)

# Buttons
vk_button = tk.Button(root, text="Virtual Keyboard", font=("Arial", 14), command=run_virtual_keyboard, width=20)
vk_button.pack(pady=10)

paint_button = tk.Button(root, text="Paint", font=("Arial", 14), command=run_paint, width=20)
paint_button.pack(pady=10)

# Run the GUI loop
root.mainloop()
