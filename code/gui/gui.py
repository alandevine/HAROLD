#!/usr/bin/python3

import PIL
import cv2
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk


class GUI:

    def __init__(self, win_name="Main", win_h=900, win_w=1600):
        self.win_name = win_name
        self.win_h = win_h
        self.win_w = win_w

        self.root = tk.Tk()
        self.root.title(self.win_name)

        # bind 'escape' to quit gui
        self.root.bind("<Escape>", lambda e: self.root.quit())

        self.main_win = tk.Label(self.root)

        # set default resolution of window
        self.root.geometry("%dx%d" % (self.win_w, self.win_h))

        # create camera windows
        self.cam_1_win = tk.Label(self.main_win)
        self.cam_2_win = tk.Label(self.main_win)

        self.object_grid = tk.Label(self.main_win)
        self.object_title = tk.Label(self.object_grid, text="Detected Objects")

        self.main_win.pack()

        self.cam_1_win.pack(padx=20, pady=20, side=tk.LEFT)
        self.cam_2_win.pack(padx=20, pady=20, side=tk.RIGHT)

        self.object_grid.pack()
        self.object_title.pack()

        self.object_dict = {}
        self.object_list = []

        self.object_dict["foo"] = ["bar"]
        self.object_dict["flu"] = ["car"]
        self.object_dict["blu"] = ["far"]
        self.object_dict["moo"] = ["tar"]

        self.update_object_list()

    def show_frame(self, camera, label):
        _, frame = camera.cam.read()

        cv2_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        img = PIL.Image.fromarray(cv2_frame)
        img = ImageTk.PhotoImage(img)

        label.imgtk = img
        label.configure(image=img)

        label.after(100, self.show_frame, camera, label)

    def gui_loop(self):
        self.root.mainloop()

    def update_object_list(self):
        """Method for updating visible list of detected objects derived from
        the object dictionary"""

        for k, v in self.object_dict.items():
            if k not in self.object_list:
                self.object_list.append(k)

                obj = ttk.Button(self.object_grid,
                                 text=k,
                                 command=lambda k=k: self.on_click_object(k))

                obj.pack()

        self.root.after(10, self.update_object_list)

    def on_click_object(self, key):
        val = self.object_dict[key]
        print(val)
        return val


class Camera:

    def __init__(self, camera_idx, view_h=450, view_w=800):
        self.cam = cv2.VideoCapture(camera_idx)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, view_h)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, view_w)

    def __del__(self):
        self.cam.release()


def main():
    try:
        root = GUI("H.A.R.O.L.D")
        cam_1 = Camera(0, 450, 800)
        cam_2 = Camera(1, 450, 800)
        root.show_frame(cam_1, root.cam_1_win)
        root.show_frame(cam_2, root.cam_2_win)
        root.gui_loop()

    except KeyboardInterrupt:
        quit()


if __name__ == "__main__":
    main()
