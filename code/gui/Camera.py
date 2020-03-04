#!/usr/bin/python3

import cv2
import numpy as np
from math import sqrt
from centroid_tracker import CentroidTracker


class Camera:

    """Camera Class
    Default values based on Playstation Eye camera"""

    def __init__(self, camera_idx, camera_view, res_x=640, res_y=480,
                 view_h=450, view_w=800, origin_distance=0):

        """
            camera_idx: refers to the device number
            camera_view: can either be "TOP-DOWN" or "FRONT-ON"
            res_x: refers to camera's horisontal resolution
            res_x: refers to camera's verical resolution
            view_h: height of the camera view window
            view_w: width of the camera view window
            origin_distance: distance between camera and origin in cm
            static_background: backgroud for which newly drawn frames are
                               diffed against for detecting objects
        """

        self.cam = cv2.VideoCapture(camera_idx)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, view_h)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, view_w)

        # where the camera view
        self.camera_view = camera_view
        assert(self.camera_view == "TOP-DOWN" or "FRONT-ON")

        self.res_x = res_x
        self.res_y = res_y

        self.origin_distance = origin_distance
        self.pixle_cm_ratio = 0

        self.static_background = None
        self.centroid_tracker = CentroidTracker()

    def object_vector(self, centroid):
        """Method for determining the vector between the mid
        point of the screen"""

        object_x = centroid[0]
        object_y = centroid[1]

        print("cam.objvec>>", object_x, object_y)

        y = object_x - self.res_x // 2

        # There may be a bit of confusion arround the variable names
        # the assigned x, y and z refer to vector co-ordinates. Otherwise
        # I am refering to the x, y position in the camera view

        if self.camera_view == "TOP-DOWN":
            x = object_y - self.res_y // 2
            z = None
        else:
            x = None
            z = object_y - self.res_y // 2

        return (x, y, z)

    def draw_bounding_boxs(self, frame):

        """Method for drawing bounding boxes arround objects different to the
        static background
        """

        diff = cv2.absdiff(self.static_background, frame)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(src=gray, ksize=(5, 5), sigmaX=0)

        rects = []

        _, thresh = cv2.threshold(src=blur,
                                  thresh=70,
                                  maxval=255,
                                  type=cv2.THRESH_BINARY)

        dilated = cv2.dilate(src=thresh, kernel=None, iterations=3)

        contours, _ = cv2.findContours(image=dilated,
                                       mode=cv2.RETR_TREE,
                                       method=cv2.CHAIN_APPROX_SIMPLE)

        for i, contour in enumerate(contours):

            (x, y, w, h) = cv2.boundingRect(contour)

            box_bounds = np.array([x, x + w, y, y + h])
            rects.append(box_bounds)

            if cv2.contourArea(contour) < 900:
                continue

            centroid = x + w // 2, y + h // 2

            cv2.rectangle(img=frame,
                          pt1=(x, y),           # bottom left coord
                          pt2=(x + w, y + h),   # top right coord
                          color=(255, 0, 0),
                          thickness=2)

            cv2.circle(img=frame,
                       center=(centroid),
                       radius=5,
                       color=(255, 0, 0),
                       thickness=2)

        object_dict = self.centroid_tracker.update_objects(rects)

        for obj_id, centroid in object_dict.items():
            text = "ID %s" % {obj_id}

            cv2.putText(frame,
                        text,
                        (centroid[0] - 10, centroid[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 255, 0),
                        2)

            cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)

        return frame, object_dict

    def __del__(self):
        self.cam.release()

    @staticmethod
    def merge_vectors(vector_a, vector_b):
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
