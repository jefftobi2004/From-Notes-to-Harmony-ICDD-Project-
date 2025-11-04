import tkinter as tk
from PIL import Image, ImageTk

def resize_image(image, max_width, max_height):
    """Resize the image to fit within max_width and max_height, preserving aspect ratio."""
    width_ratio = max_width / image.width
    height_ratio = max_height / image.height
    resize_ratio = min(width_ratio, height_ratio)
    
    new_width = int(image.width * resize_ratio)
    new_height = int(image.height * resize_ratio)
    return image.resize((new_width, new_height), Image.LANCZOS)

# Create a Tkinter window
root = tk.Tk()
root.title("Piano Interface")

# Load the image
image_path = "images/keys.png"  
original_image = Image.open(image_path)

# Define the maximum dimensions for the window (you can adjust these)
max_window_width = root.winfo_screenwidth() 
max_window_height = root.winfo_screenheight()

# Resize the image to fit within the maximum dimensions
resized_image = resize_image(original_image, max_window_width, max_window_height)

# Convert the resized image to a format that Tkinter can use
tk_image = ImageTk.PhotoImage(resized_image)

# Set the window size to the resized image dimensions
root.geometry(f"{resized_image.width}x{resized_image.height}")

# Create a label to display the image
label = tk.Label(root, image=tk_image)
label.pack()

# Run the Tkinter event loop
root.mainloop()
