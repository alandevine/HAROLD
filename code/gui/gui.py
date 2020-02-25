#!/usr/bin/python3

import asyncio
import PIL
import cv2
import tkinter as tk
from PIL import ImageTk


class GUI:

    def __init__(self, win_name="Main", win_h=900, win_w=1600):
        self.win_name = win_name
        self.win_h = win_h
        self.win_w = win_w

        self.root = tk.Tk()
        self.root.bind('<Escape>', lambda e: self.root.quit())

        self.main_win = tk.Label(self.root)
        self.main_win.pack()

    def show_frame(self, camera):
        _, frame = camera.cam.read()

        frame = cv2.flip(frame, 1)

        cv2_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        img = PIL.Image.fromarray(cv2_frame)
        img = ImageTk.PhotoImage(img)

        self.main_win.imgtk = img
        self.main_win.configure(image=img)

        self.main_win.after(10, self.show_frame, camera)

    def gui_loop(self):
        self.root.mainloop()


class Camera:

    def __init__(self, camera_idx, view_h, view_w):
        self.cam = cv2.VideoCapture(camera_idx)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, view_h)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, view_w)

    def __del__(self):
        self.cam.release()


def main():
    try:
        root = GUI("test")
        cam = Camera(0, 450, 800)
        root.show_frame(cam)
        root.gui_loop()

    except KeyboardInterrupt:
        quit()


if __name__ == "__main__":
    main()
