import tkinter as tk
from screeninfo import get_monitors

# Define lighting presets with common video lighting colors
LIGHT_PRESETS = {
    "Cool White": "#E0FFFF",  # Icy blue white
    "Neutral White": "#FFFFFF",  # Pure white
    "Warm White": "#FFF5E1",  # Soft yellow white
    "Soft Red": "#FFB3B3",  # Warm soft red
    "Orange/Amber": "#FFCC99",  # Amber light
    "Soft Blue": "#ADD8E6",  # Light blue
    "Lavender Purple": "#D8BFD8"  # Soft purple
}

# Create main window
root = tk.Tk()
root.attributes("-topmost", True)  # Keep on top
root.overrideredirect(True)  # Remove window borders

# Get full screen dimensions across all monitors
total_width = sum(monitor.width for monitor in get_monitors())
total_height = max(monitor.height for monitor in get_monitors())

# Make the window span across all monitors
root.geometry(f"{total_width}x{total_height}+0+0")
root.configure(bg=LIGHT_PRESETS["Neutral White"])  # Default background color

# Smooth fade transition effect
def fade_to_color(target_color, step=5):
    """Gradually fade from the current color to the target color."""
    current_color = root["bg"]
    
    # Convert HEX color to RGB
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    # Convert RGB back to HEX
    def rgb_to_hex(rgb):
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

    start_rgb = hex_to_rgb(current_color)
    end_rgb = hex_to_rgb(target_color)

    def update_color(step_count=0):
        if step_count >= step:
            root.configure(bg=target_color)
            return

        new_rgb = tuple(
            int(start_rgb[i] + (end_rgb[i] - start_rgb[i]) * (step_count / step))
            for i in range(3)
        )
        root.configure(bg=rgb_to_hex(new_rgb))
        root.after(30, update_color, step_count + 1)  # Adjust timing for smooth transition

    update_color()

# Toolbar Frame (Dark Modern Look)
toolbar = tk.Frame(root, bg="#2D2D2D", height=50)
toolbar.pack(fill="x", side="top", anchor="nw")

# Create color selection buttons
button_size = 40  # Square buttons
for color_name, hex_color in LIGHT_PRESETS.items():
    button = tk.Button(
        toolbar,
        bg=hex_color,
        width=3,
        height=2,
        relief="flat",
        command=lambda c=hex_color: fade_to_color(c)
    )
    button.pack(side="left", padx=5, pady=5)

# Exit button
exit_button = tk.Button(toolbar, text="❌", bg="#555", fg="white", command=root.destroy, relief="flat")
exit_button.pack(side="right", padx=10, pady=5)

# Bind ESC key to exit
root.bind("<Escape>", lambda event: root.destroy())

# Run the application
root.mainloop()
