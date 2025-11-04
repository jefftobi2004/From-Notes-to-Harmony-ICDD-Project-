import tkinter as tk
from PIL import Image, ImageTk
import mido
import connection
import threading

WINDOW_HEIGHT = 800
WINDOW_WIDTH = 1913

# Setting the paths of the images
base_image_path = "images/keys.png"
key_left_path = "images/key_green_left.png"
key_mid_path = "images/key_green_mid.png"
key_right_path = "images/key_green_right.png"
key_top_path = "images/key_green_top.png"

# Loading the images
base_image = Image.open(base_image_path)
key_left = Image.open(key_left_path)
key_mid = Image.open(key_mid_path)
key_right = Image.open(key_right_path)
key_top = Image.open(key_top_path)

key_positions = {
    36: ((3, 1067), 'white_left'),
    37: ((52, 1067), 'black_top'),
    38: ((71, 1067), 'white_mid'),
    39: ((120, 1067), 'black_top'),
    40: ((139, 1067), 'white_right'),
    41: ((207, 1067), 'white_left'),
    42: ((256, 1067), 'black_top'),
    43: ((275, 1067), 'white_mid'),
    44: ((324, 1067), 'black_top'),
    45: ((343, 1067), 'white_mid'),
    46: ((393, 1067), 'black_top'),
    47: ((412, 1067), 'white_right'),
    48: ((480, 1067), 'white_left'),
    49: ((529, 1067), 'black_top'),
    50: ((548, 1067), 'white_mid'),
    51: ((597, 1067), 'black_top'),
    52: ((616, 1067), 'white_right'),
    53: ((685, 1067), 'white_left'),
    54: ((733, 1067), 'black_top'),
    55: ((753, 1067), 'white_mid'),
    56: ((802, 1067), 'black_top'),
    57: ((821, 1067), 'white_mid'),
    58: ((870, 1067), 'black_top'),
    59: ((889, 1067), 'white_right'),
    60: ((958, 1067), 'white_left'),
    61: ((1007, 1067), 'black_top'),
    62: ((1026, 1067), 'white_mid'),
    63: ((1075, 1067), 'black_top'),
    64: ((1094, 1067), 'white_right'),
    65: ((1163, 1067), 'white_left'),
    66: ((1211, 1067), 'black_top'),
    67: ((1231, 1067), 'white_mid'),
    68: ((1280, 1067), 'black_top'),
    69: ((1299, 1067), 'white_mid'),
    70: ((1348, 1067), 'black_top'),
    71: ((1367, 1067), 'white_right'),
    72: ((1436, 1067), 'white_left'),
    73: ((1485, 1067), 'black_top'),
    74: ((1504, 1067), 'white_mid'),
    75: ((1553, 1067), 'black_top'),
    76: ((1572, 1067), 'white_right'),
    77: ((1640, 1067), 'white_left'),
    78: ((1689, 1067), 'black_top'),
    79: ((1709, 1067), 'white_mid'),
    80: ((1757, 1067), 'black_top'),
    81: ((1776, 1067), 'white_mid'),
    82: ((1825, 1067), 'black_top'),
    83: ((1845, 1067), 'white_right')
}

highlighted_keys = {
    'white_left': key_left,
    'white_mid': key_mid,
    'white_right': key_right,
    'black_top': key_top,
}

pressed_keys = set()

def overlay_key(base_image, key_type, position):
    highlighted_key = highlighted_keys[key_type]
    temp_image = base_image.copy()
    temp_image.paste(highlighted_key, position, highlighted_key)
    return temp_image

def on_midi_message(msg):
    global pressed_keys
    if msg.type in ['note_on', 'note_off']:
        note = msg.note
        if 36 <= note <= 84:  # Ensure the note is within the range
            if msg.type == 'note_on' and msg.velocity > 0:
                pressed_keys.add(note)
            else:
                pressed_keys.discard(note)
            temp_image = base_image.copy()
            for note in pressed_keys:
                position, key_type = key_positions[note]
                temp_image = overlay_key(temp_image, key_type, position)
            update_image(temp_image)

def update_image(image):
    tk_image = ImageTk.PhotoImage(image)
    label.config(image=tk_image)
    label.image = tk_image

def main():
    global label, root

    root = tk.Tk()
    root.title("Piano Key Visualizer")

    tk_base_image = ImageTk.PhotoImage(base_image)
    label = tk.Label(root, image=tk_base_image)
    label.image = tk_base_image 
    label.pack()

    # Start separate threads for MIDI handling for the interface and printing to terminal
    thread_interface = threading.Thread(target=midi_thread, daemon=True)
    #thread_terminal = threading.Thread(target=print_thread, daemon=True)
    thread_interface.start()
    #thread_terminal.start()

    root.mainloop()

def midi_thread():
    connection.handle_midi_messages(on_midi_message)

def print_thread():
    connection.handle_midi_messages(connection.show_information)

if __name__ == "__main__":
    main()