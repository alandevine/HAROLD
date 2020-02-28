#!/usr/bin/python3

from PIL import ImageTk
from math import sqrt
from tkinter import ttk
import PIL
import cv2
import tkinter as tk


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

    """Camera Class
    Default values based on Playstation Eye camera"""

    def __init__(self, camera_idx, camera_view, res_x=640, res_y=480,
                 view_h=450, view_w=800):

        """
            camera_idx: refers to the device number
            camera_view: can either be "TOP-DOWN" or "FRONT-ON"
            res_x: refers to camera's horisontal resolution
            res_x: refers to camera's verical resolution
            view_h: height of the camera view window
            view_h: width of the camera view window
        """

        self.cam = cv2.VideoCapture(camera_idx)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, view_h)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, view_w)

        # where the camera view
        self.camera_view = camera_view
        assert(self.camera_view == "TOP-DOWN" or "FRONT-ON")

        self.res_x = res_x
        self.res_y = res_y

    def object_vector(self, object_x, object_y):
        """Method for determining the vector between the mid
        point of the screen"""

        y = object_x - self.cam.res_x // 2

        # There may be a bit of confusion arround the variable names
        # the assigned x, y and z refer to vector co-ordinates. Otherwise
        # I am refering to the x, y position in the camera view

        if self.camera_view == "TOP-DOWN":
            x = object_y - self.cam.res_y // 2
            z = None
        else:
            x = None
            z = object_y - self.cam.res_y // 2

        return (x, y, z)

    def __del__(self):
        self.cam.release()

    @staticmethod
    def merge_vectors(self, vector_a, vector_b):
        """Static method for merging 2 given vectors
        inputs come in tuple form with the assumption that both x values
        will be equal, due to the decided upon camera layout.
        """

        n_x = vector_a[0]
        n_y = vector_a[1] if vector_a[1] is not None else vector_b[1]
        n_z = vector_a[2] if vector_a[2] is not None else vector_b[2]

        return (n_x, n_y, n_z)

    @staticmethod
    def vector_distance(self, v):
        return sqrt([i ** 2 for i in v])


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

        root.show_frame(cam_1, root.cam_1_win)
        root.show_frame(cam_2, root.cam_2_win)
        root.gui_loop()

    except KeyboardInterrupt:
        quit()


if __name__ == "__main__":
    main()
