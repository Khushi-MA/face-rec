import tkinter as tk
import subprocess

def run_virtual_keyboard():
    subprocess.Popen(['python', 'virtualkey2.py'])

def run_paint():
    subprocess.Popen(['python', 'paint1.py'])

# Create main window
root = tk.Tk()
root.title("Hand Gesture Project")
root.geometry("1280x720")
root.configure(bg="#e6f2ff")  # Soft blue background

# Styling variables
button_font = ("Helvetica", 18, "bold")
title_font = ("Helvetica", 32, "bold")
button_width = 25
button_height = 2
button_color = "#3399ff"
button_fg = "#ffffff"
hover_color = "#2673cc"

# Title label
title_label = tk.Label(root, text="🎯 Hand Gesture Project 🎯", font=title_font, bg="#e6f2ff", fg="#003366")
title_label.pack(pady=60)

# Function to change button color on hover
def on_enter(e):
    e.widget['background'] = hover_color

def on_leave(e):
    e.widget['background'] = button_color

# Virtual Keyboard Button
vk_button = tk.Button(root, text="🧠 Virtual Keyboard", font=button_font, command=run_virtual_keyboard,
                      width=button_width, height=button_height, bg=button_color, fg=button_fg, bd=0, activebackground=hover_color)
vk_button.pack(pady=20)
vk_button.bind("<Enter>", on_enter)
vk_button.bind("<Leave>", on_leave)

# Paint Button
paint_button = tk.Button(root, text="🎨 Gesture Paint", font=button_font, command=run_paint,
                         width=button_width, height=button_height, bg=button_color, fg=button_fg, bd=0, activebackground=hover_color)
paint_button.pack(pady=20)
paint_button.bind("<Enter>", on_enter)
paint_button.bind("<Leave>", on_leave)

# Run the GUI loop
root.mainloop()
