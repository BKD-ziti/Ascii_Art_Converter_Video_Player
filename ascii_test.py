import cv2
import tkinter as tk
from tkinter import filedialog

window_width = 720
window_height = 480

root = tk.Tk()
root.title("ASCII Video Player")
root.geometry(f"{window_width}x{window_height}")

ASCII_CHARS = "@%#*+=-:. &?<>\{[]}"

ascii_label = tk.Label(root, font=("Courier New", 8))
ascii_label.pack()

cap = None
paused = False

def frame_to_ascii(frame, width=100):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY)
    frame = cv2.resize(frame, (width, int(frame.shape[0] * (width / frame.shape[1])))
    )
    ascii_frame = ''
    for row in frame:
        for pixel_value in row:
            ascii_frame += ASCII_CHARS[int(pixel_value * (len(ASCII_CHARS) - 1) / 255)]
        ascii_frame += '\n'

    lines = []
    line = ''
    for char in ascii_frame:
        if char == '\n':
            lines.append(line)
            line = ''
        else:
            line += char
    return '\n'.join(lines)

def update_ascii_frame(video_path):
    global cap, paused
    if cap is None:
        cap = cv2.VideoCapture(video_path)
    if not paused:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        else:
            ascii_frame = frame_to_ascii(frame)
            ascii_label.config(text=ascii_frame)
    root.after(10, update_ascii_frame, video_path)

def open_video_file():
    global cap
    file_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
    if file_path:
        cap = None
        update_ascii_frame(file_path)

def play_pause():
    global paused
    paused = not paused

open_button = tk.Button(root, text="Open Video File", command=open_video_file)
open_button.pack()

play_pause_button = tk.Button(root, text="Play/Pause", command=play_pause)
play_pause_button.pack()

def quit_app():
    global cap
    if cap is not None:
        cap.release()
    root.destroy()

quit_button = tk.Button(root, text="Quit", command=quit_app)
quit_button.pack()

root.mainloop()
