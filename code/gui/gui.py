#!/usr/bin/python3

from Camera import Camera
from PIL import ImageTk
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

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        diff = cv2.absdiff(camera.static_background, frame)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(src=gray, ksize=(5, 5), sigmaX=0)

        _, thresh = cv2.threshold(src=blur,
                                  thresh=70,
                                  maxval=255,
                                  type=cv2.THRESH_BINARY)

        dilated = cv2.dilate(thresh, kernel=None, iterations=3)

        contours, _ = cv2.findContours(image=dilated,
                                       mode=cv2.RETR_TREE,
                                       method=cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            if cv2.contourArea(contour) < 900:
                continue

            cv2.rectangle(frame,
                          pt1=(x, y),
                          pt2=(x + w, y + h),
                          color=(255, 0, 0),
                          thickness=2)

            cv2.circle(frame,
                       center=(x + w // 2, y + h // 2),
                       radius=5,
                       color=(255, 0, 0),
                       thickness=2)

        img = PIL.Image.fromarray(frame)
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
