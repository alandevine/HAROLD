#!/usr/bin/python3

from Camera import Camera
from PIL import ImageTk
from collections import OrderedDict
from tkinter import ttk
import PIL
import cv2
import os
import tkinter as tk


class CameraSetup:
    """Choose camera and default settings"""

    def __init__(self, win_name="Camera Setup", win_h=900, win_w=1600,
                 frame_delay=100):
        self.win_name = win_name
        self.win_h = win_h
        self.win_w = win_w
        self.frame_delay = frame_delay

        self.root = tk.Tk()
        self.root.title(self.win_name)
        self.root.bind("<Escape>", lambda e: self.root.quit())

        self.root.geometry("%dx%d" % (self.win_w, self.win_h))

        self.main_win = tk.Frame(self.root)
        # self.main_win = tk.Label(self.root)

        self.main_win.pack()

        # List cameras
        cameras = list_cameras()
        cameras_positions = ["TOP-DOWN", "FRONT-ON"]

        self.cam_1_path = tk.StringVar(self.root)
        self.cam_2_path = tk.StringVar(self.root)

        self.cam_1_path.set(cameras[0])
        self.cam_2_path.set(cameras[1])


        print(self.cam_1_path)
        print(self.cam_1_path.get())

        self.cam_1_pos = tk.StringVar(self.root)
        self.cam_2_pos = tk.StringVar(self.root)

        self.cam_1_pos.set(cameras_positions[0])
        self.cam_2_pos.set(cameras_positions[1])

        # Create GUI elements
        self.cam_1_win = tk.Label(self.main_win)
        self.cam_2_win = tk.Label(self.main_win)

        self.exit_button = tk.Button(self.main_win,
                                     text="Ok",
                                     command=lambda: self.root.quit())

        self.select_cam_1 = tk.OptionMenu(self.main_win,
                                          self.cam_1_path,
                                          *cameras)

        self.select_cam_2 = tk.OptionMenu(self.main_win,
                                          self.cam_2_path,
                                          *cameras)

        self.select_cam_1_pos = tk.OptionMenu(self.main_win,
                                              self.cam_1_pos,
                                              *cameras_positions)

        self.select_cam_2_pos = tk.OptionMenu(self.main_win,
                                              self.cam_2_pos,
                                              *cameras_positions)

        # Draw gui elements on screen
        self.cam_1_win.grid(row=0, column=0)
        self.select_cam_1.grid(row=1, column=0)
        self.select_cam_1_pos.grid(row=2, column=0)

        self.cam_2_win.grid(row=0, column=2)
        self.select_cam_2.grid(row=1, column=2)
        self.select_cam_2_pos.grid(row=2, column=2)

        self.exit_button.grid(row=3, column=1)

        self.cam_1 = Camera(self.cam_1_path.get(), self.cam_1_pos.get())
        self.cam_2 = Camera(self.cam_2_path.get(), self.cam_1_pos.get())

        self.show_frame(self.cam_1, self.cam_1_win)
        self.show_frame(self.cam_2, self.cam_2_win)

        self.root.mainloop()
    
    def show_frame(self, camera, label):
        _, frame = camera.cam.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = ImageTk.PhotoImage(PIL.Image.fromarray(frame),
                                 master=self.main_win)

        label.imgtk = img
        label.configure(image=img)

        camera.static_background = frame

        label.after(self.frame_delay, self.show_frame, camera, label)

    def return_cameras(self):
        return self.cam_1, self.cam_2


class MainWindow:
    """Main Class for the User Interface"""

    def __init__(self, win_name="Main", win_h=900,
                 win_w=1600, frame_delay=100):

        self.win_name = win_name

        # vertical resolution
        self.win_h = win_h

        # horizontal resolution
        self.win_w = win_w

        # delay between frames
        self.frame_delay = frame_delay

        self.root = tk.Tk()
        self.root.title(self.win_name)

        # bind 'escape' to quit gui
        self.root.bind("<Escape>", lambda e: self.root.quit())

        # creates a window with in the root
        self.main_win = tk.Frame(self.root)

        # set default resolution of window
        self.root.geometry("%dx%d" % (self.win_w, self.win_h))

        # create camera windows
        self.cam_1_win = tk.Label(self.main_win)
        self.cam_2_win = tk.Label(self.main_win)

        # list of buttons that interact with a dictionary
        self.object_space = tk.Frame(self.main_win)
        self.object_title = tk.Label(self.object_space, text="detected objects")

        # apply window components to the main window
        self.main_win.pack()

        # apply styling to camera windows while applying them to main window
        self.cam_1_win.grid(row=0, column=0)
        self.cam_2_win.grid(row=0, column=2)

        self.object_space.grid(row=1, column=1)
        self.object_title.grid(row=1, column=1)

        self.object_dict = OrderedDict()
        self.object_list = []

        self.update_object_list()

    def show_frame(self, camera, label):
        """Method for showing a single camera frame
        in addition to showing a frame, the detected objects (objects that
        do not appear in the background frame defined in the Camera class
        will be given a bounding box as well as centroid

        This method will call itself after 100ms
        """

        _, frame = camera.cam.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if camera.static_background is not None:
            frame, objects = camera.draw_bounding_boxs(frame)

            for obj_id, part_vec_a in objects.items():
                # object id's are distributed left to right of the given frame

                if obj_id in self.object_dict.keys():
                    # if there is already a vector with this id
                    partial_vector = self.object_dict[obj_id]
                    self.object_dict[obj_id] = Camera.merge_vectors(
                                                    partial_vector, part_vec_a)

                else:
                    self.object_dict[obj_id] = part_vec_a

        img = ImageTk.PhotoImage(PIL.Image.fromarray(frame),
                                 master=self.main_win)

        label.imgtk = img
        label.configure(image=img)

        label.after(self.frame_delay, self.show_frame, camera, label)

    def gui_loop(self):
        self.root.mainloop()

    def update_object_list(self):
        """Method for updating visible list of detected objects derived from
        the object dictionary"""

        for k, v in self.object_dict.items():
            if k not in self.object_list:
                self.object_list.append(k)

                obj = ttk.Button(self.main_win,
                                 text=k,
                                 command=lambda k=k: self.on_click_object(k))

                obj.grid(row=len(self.object_list) + 1, column=1)

        self.root.after(self.frame_delay, self.update_object_list)

    def on_click_object(self, key):
        val = self.object_dict[key]
        print(val)
        return val


def list_cameras():

    """Function for listing all video sources connected to the computer
    This will only work on linux/ mac os devices
    """

    cameras = []
    for device in os.listdir("/dev/"):
        # Cameras follow the format "videoX" where X is the device number
        if device[:5].lower() == "video":
            # append the path to the device
            cameras.append("/dev/" + device)

    return cameras


def main():
    try:
        setup = CameraSetup()
        cam_1, cam_2 = setup.return_cameras()
        setup.root.destroy()

        root = MainWindow("H.A.R.O.L.D")

        root.show_frame(cam_1, root.cam_1_win)
        root.show_frame(cam_2, root.cam_2_win)
        root.gui_loop()
    except KeyboardInterrupt:
        quit()


if __name__ == "__main__":
    main()
