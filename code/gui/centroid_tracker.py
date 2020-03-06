#!/usr/bin/python3

from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np


class CentroidTracker():

    def __init__(self, frame_threshold=20):

        # unique object id
        self.current_obj_id = 0

        # dictionary containing object id's and co-ordinates on-screen
        self.objects = OrderedDict()

        # dictionary containing object id's and number of frames it has
        # been out view
        self.frames_elapsed = OrderedDict()

        # number of frames an object can be out of view before being deleted
        # the default being 48 frames which roughly corresponds to 2 seconds
        self.frame_threshold = frame_threshold

    def add_object(self, centroid):
        self.objects[self.current_obj_id] = centroid
        self.frames_elapsed[self.current_obj_id] = 0
        self.current_obj_id += 1

    def del_object(self, obj_id):
        # delete objects from both dictionary's
        del self.objects[obj_id]
        del self.frames_elapsed[obj_id]

    def increment_frame(self, obj_id):
        self.frames_elapsed[obj_id] += 1
        if self.frames_elapsed[obj_id] > self.frame_threshold:
            self.del_object(obj_id)

    def update_objects(self, rects):

        # in the case that all objects are missing, we will increment
        # all object frames

        if len(rects) == 0:
            for obj_id in list(self.frames_elapsed.keys()):
                self.increment_frame(obj_id)

            return self.objects

        # initialize an array of input centroids for the current frame
        new_centroids = np.zeros((len(rects), 2), dtype="int")

        # loop over the bounding box rectangles
        for i, (x1, x2, y1, y2) in enumerate(rects):
            # use the bounding box coordinates to derive the centroid
            n_x = (x1 + x2) // 2
            n_y = (y1 + y2) // 2
            new_centroids[i] = (n_x, n_y)

        # if we are currently not tracking any objects take the input
        # centroids and add_object each of them
        if len(self.objects) == 0:
            for i in range(0, len(new_centroids)):
                self.add_object(new_centroids[i])

        # otherwise, are are currently tracking objects so we need to
        # try to match the input centroids to existing object
        # centroids
        else:
            # grab the set of object IDs and corresponding centroids
            all_obj_ids = list(self.objects.keys())
            all_obj_centroids = list(self.objects.values())

            # compute the distance between each pair of object
            # centroids and input centroids, respectively -- our
            # goal will be to match an input centroid to an existing
            # object centroid
            D = dist.cdist(np.array(all_obj_centroids), new_centroids)

            # in order to perform this matching we must (1) find the
            # smallest value in each row and then (2) sort the row
            # indexes based on their minimum values so that the row
            # with the smallest value as at the *front* of the index
            # list
            rows = D.min(axis=1).argsort()

            # next, we perform a similar process on the columns by
            # finding the smallest value in each column and then
            # sorting using the previously computed row index list
            cols = D.argmin(axis=1)[rows]

            # in order to determine if we need to update_objects, add_object,
            # or del_object an object we need to keep track of which
            # of the rows and column indexes we have already examined
            used_rows = set()
            used_cols = set()

            # loop over the combination of the (row, column) index
            # tuples
            for (row, col) in zip(rows, cols):
                # if we have already examined either the row or
                # column value before, ignore it
                # val
                if row in used_rows or col in used_cols:
                    continue

                # otherwise, grab the object ID for the current row,
                # set its new centroid, and reset the frames_elapsed
                # counter
                obj_id = all_obj_ids[row]
                self.objects[obj_id] = new_centroids[col]
                self.frames_elapsed[obj_id] = 0

                # indicate that we have examined each of the row and
                # column indexes, respectively
                used_rows.add(row)
                used_cols.add(col)

            # compute both the row and column index we have NOT yet
            # examined
            unused_rows = set(range(0, D.shape[0])).difference(used_rows)
            unused_cols = set(range(0, D.shape[1])).difference(used_cols)

            # in the event that the number of object centroids is
            # equal or greater than the number of input centroids
            # we need to check and see if some of these objects have
            # potentially frames_elapsed
            if D.shape[0] >= D.shape[1]:
                # loop over the unused row indexes
                for row in unused_rows:
                    # grab the object ID for the corresponding row
                    # index and increment the frames_elapsed counter
                    obj_id = all_obj_ids[row]
                    self.frames_elapsed[obj_id] += 1

                    # check to see if the number of consecutive
                    # frames the object has been marked "frames_elapsed"
                    # for warrants deregistering the object
                    if self.frames_elapsed[obj_id] > self.frame_threshold:
                        self.del_object(obj_id)

            # otherwise, if the number of input centroids is greater
            # than the number of existing object centroids we need to
            # add_object each new input centroid as a trackable object
            else:
                for col in unused_cols:
                    self.add_object(new_centroids[col])

        # return the set of trackable objects
        return self.objects
