import cv2
import tkinter as tk
from tkinter import filedialog

window_width = 800
window_height = 800

root = tk.Tk()
root.title("ASCII Video Player")

ASCII_CHARS = "@%#*+=-:. &?<>\{[]}"

# Initialize variables inside the function where cap is defined
cap = None
original_frame_rate = 0
desired_frame_rate = 30
frame_delay = int(1000 / desired_frame_rate)  # Delay in milliseconds

# Flag to indicate whether the video is playing or paused
is_playing = True

def update_ascii_frame(video_path):
    global cap, original_frame_rate, is_playing

    if cap is None:
        cap = cv2.VideoCapture(video_path)
        original_frame_rate = cap.get(cv2.CAP_PROP_FPS)  # Get the original frame rate here

    if is_playing:
        ret, frame = cap.read()

        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        else:
            ascii_frame = frame_to_ascii(frame)
            ascii_label.config(text=ascii_frame)

    root.after(frame_delay, update_ascii_frame, video_path)

# Function to convert a frame to ASCII art with word wrap
def frame_to_ascii(frame, width=100, line_width=50):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Resize the frame to half of its original size while keeping the aspect ratio
    aspect_ratio = frame.shape[1] / frame.shape[0]
    new_width = int(width / 2)
    new_height = int(new_width / aspect_ratio)
    frame = cv2.resize(frame, (new_width, new_height))
    ascii_frame = ''
    for row in frame:
        for pixel_value in row:
            # Adjust the range based on the number of characters in ASCII_CHARS
            ascii_frame += ASCII_CHARS[int(pixel_value * (len(ASCII_CHARS) - 1) / 255)]
        ascii_frame += '\n'  # Add a newline at the end of each row

    # Split the ASCII art into lines
    lines = []
    line = ''
    for char in ascii_frame:
        if char == '\n':
            lines.append(line)
            line = ''
        else:
            line += char

    # Join the lines with newline characters
    return '\n'.join(lines)

# Create a Tkinter label to display the ASCII art
ascii_label = tk.Label(root, font=("Courier", 6))
ascii_label.pack()

def stop_video():
    global is_playing
    is_playing = False

def play_video():
    global is_playing
    is_playing = True

# Function to open a file dialog and get the selected video file path
def open_video_file():
    global is_playing, cap
    is_playing = True
    file_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
    if file_path:
        cap = cv2.VideoCapture(file_path)  # Initialize the global cap variable
        update_ascii_frame(file_path)  # Update ASCII art with the selected video
        # Set the window size based on the resized frame dimensions
        frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        root.geometry(f"{int(frame_width)}x{int(frame_height)}")

# Create an Open File button
open_button = tk.Button(root, text="Open Video File", command=open_video_file)
open_button.pack()

# Create a Play button
play_button = tk.Button(root, text="Play", command=play_video)
play_button.pack()

# Create a Stop button
stop_button = tk.Button(root, text="Stop", command=stop_video)
stop_button.pack()

# Function to quit the application
def quit_app():
    global cap
    if cap is not None:
        cap.release()  # Release the video capture object if it exists
    root.destroy()
    exit()

# Create a Quit button
quit_button = tk.Button(root, text="Quit", command=quit_app)
quit_button.pack()

root.mainloop()
