#!/usr/bin/python3

import cv2
from math import sqrt


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
            origin_distance: distance between camera and origin in mm
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
