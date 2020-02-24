#!/usr/bin/python3

import cv2
import tkinter as tk


class MainWindow:

    def __init__(self, name, height, width):
        self.name = name
        self.height = height
        self.width = width

    def make_window(self):
        window = tk.Tk()
        window.title(self.name)
        window.geometry("%dx%d" % (self.height, self.width))
        return window


class CameraWidget:

    def __init__(self, camera_idx=0, fps=24, widget_h=800, widget_w=450):
        cam = cv2.VideoCapture(camera_idx)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, widget_h)
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, widget_w)


def main():
    win = MainWindow("test", 1600, 900)
    window = win.make_window()
    window.mainloop()


if __name__ == "__main__":
    main()
