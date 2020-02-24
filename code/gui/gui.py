#!/usr/bin/python3

import cv2
import threading
import PIL
from PIL import ImageTk
import tkinter as tk


class MainWindow:

    def __init__(self, name, height, width):
        self.name = name
        self.height = height
        self.width = width

        self.window = tk.Tk()

        self.panel_cam_1 = None
        self.panel_cam_2 = None

        self.window.title(self.name)

        self.cam_view_1 = cv2.VideoCapture(0)
        self.cam_view_2 = cv2.VideoCapture(1)

        cam_thread = threading.Thread(target=self.update_video, args=())

        self.canvas = tk.Canvas(self.window,
                                width=self.width,
                                height=self.height)

        self.canvas.pack()

        cam_thread.start()

        self.window.geometry("%dx%d" % (self.height, self.width))

        self.window.mainloop()

    def update_video(self):
        while True:
            ret_1, frame_1 = self.cam_view_1.read()
            ret_2, frame_2 = self.cam_view_2.read()

            photo_1 = ImageTk.PhotoImage(image=PIL.Image.fromarray(frame_1))
            photo_2 = ImageTk.PhotoImage(image=PIL.Image.fromarray(frame_2))

            photo_1 = cv2.cvtColor(frame_1, cv2.COLOR_BGR2RGB)
            photo_2 = cv2.cvtColor(frame_2, cv2.COLOR_BGR2RGB)

            if self.panel_cam_1 is None:
                self.panel_cam_1 = tk.Label(image=photo_1)
                self.panel_cam_1.image = photo_1
                self.panel_cam_1.pack(side="left", padx=10, pady=10)

            else:
                self.panel_cam_1.configure(image=photo_1)
                self.panel_cam_1.image = photo_1

            if self.panel_cam_2 is None:
                self.panel_cam_2 = tk.Label(image=photo_2)
                self.panel_cam_2.image = photo_2
                self.panel_cam_2.pack(side="right", padx=10, pady=10)

            else:
                self.panel_cam_2panel.configure(image=photo_2)
                self.panel_cam_2.image = photo_2


def main():
    window = MainWindow("test", 1600, 900)


if __name__ == "__main__":
    main()
