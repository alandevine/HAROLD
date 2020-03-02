#!/usr/bin/python3

import PIL
import cv2
import tkinter as tk
from Camera import Camera
from collections import defaultdict
from PIL import ImageTk
from tkinter import ttk


class GUI:
    """Main Class for the User Interface"""

    def __init__(self, win_name="Main", win_h=900, win_w=1600):
        self.win_name = win_name

        # vertical resolution
        self.win_h = win_h

        # horizontal resolution
        self.win_w = win_w

        self.root = tk.Tk()
        self.root.title(self.win_name)

        # bind 'escape' to quit gui
        self.root.bind("<Escape>", lambda e: self.root.quit())

        # Creates a window with in the root
        self.main_win = tk.Label(self.root)

        # set default resolution of window
        self.root.geometry("%dx%d" % (self.win_w, self.win_h))

        # create camera windows
        self.cam_1_win = tk.Label(self.main_win)
        self.cam_2_win = tk.Label(self.main_win)

        # list of buttons that interact with a dictionary
        self.object_grid = tk.Label(self.main_win)
        self.object_title = tk.Label(self.object_grid, text="Detected Objects")

        # apply window components to the main window
        self.main_win.pack()

        # apply styling to camera windows while applying them to main window
        self.cam_1_win.pack(padx=20, pady=20, side=tk.LEFT)
        self.cam_2_win.pack(padx=20, pady=20, side=tk.RIGHT)

        self.object_grid.pack()
        self.object_title.pack()

        self.object_dict = defaultdict(tuple)
        self.object_list = []

        self.object_dict["foo"] = ["bar"]
        self.object_dict["flu"] = ["car"]
        self.object_dict["blu"] = ["far"]
        self.object_dict["moo"] = ["tar"]

        self.update_object_list()

    def show_frame(self, camera, label):
        """Method for showing a single camera frame
        in addition to showing a frame, the detected objects (objects that
        do not apear in the background frame defined in the Camera class
        will be given a bounding box as well as centroid

        This method will call itself after 100ms
        """

        _, frame = camera.cam.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        bounding_box_frame, objects = camera.draw_bounding_boxs(frame)

        for k, v in objects.items():
            # object id's ar distributed left to right of the given frame

            if self.object_dict[k]:
                partial_vector = self.object_dict[k]
                self.object_dict[k] = Camera.merge_vectors(partial_vector, v)

            else:
                self.object_dict[k] = v

        img = ImageTk.PhotoImage(PIL.Image.fromarray(bounding_box_frame))

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


def main():
    try:
        root = GUI("H.A.R.O.L.D")

        cam_1 = Camera(camera_idx=0,

                       # This should be replaced with an init function
                       # when gui is launched due to usb device priority
                       camera_view="TOP-DOWN",
                       view_h=450, view_w=800)

        cam_2 = Camera(camera_idx=1,
                       camera_view="FRONT-ON",
                       view_h=450, view_w=800)

        input("Clear background, press 'Enter' to continue...")
        _, frame1 = cam_1.cam.read()
        _, frame2 = cam_2.cam.read()

        cam_1.static_background = frame1
        cam_2.static_background = frame2

        root.show_frame(cam_1, root.cam_1_win)
        root.show_frame(cam_2, root.cam_2_win)
        root.gui_loop()

    except KeyboardInterrupt:
        quit()


if __name__ == "__main__":
    main()
