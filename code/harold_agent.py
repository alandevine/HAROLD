#!/usr/bin/python3

import gym
import time
from environment.HAROLD.envs.harold_env import HaroldEnv
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2d, MaxPooling2D, Activation, Flatten
from keras.callbacks import TensorBoard
from keras.optimizers import Adam
from collections import deque

REPLAY_MEMORY_SIZE = 50000
MODEL_NAME = "256x2"


class HaroldAgent():

    """

    """

    def __init__(self):
        # Environment
        self.env = HaroldEnv()

        # Primary Model - model that gets trained
        self.model = self.create_model()

        # Target Model - model that is predicted against
        self.target_model = self.create_model()
        self.target_model.set_weights(self.model.get_weights())

        self.replay_memory = deque(maxlen=REPLAY_MEMORY_SIZE)

        self.tensorboard = ModifiedTensorBoard(log_dir=f"logs/{MODEL_NAME}-{int(time.time)}")

        self.target_update_counter = 0

    def create_model(self):
        model = Sequential()
        model.add(Conv2d(256,
                         (3, 3),
                         input_shape=self.env.OBSERVATION_SPACE_VALUES))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(2, 2))
        model.add(Dropout(0.2))

        model.add(Conv2d(256, (3, 3)))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(2, 2))
        model.add(Dropout(0.2))

        model.add(Flatten())
        model.add(Dense(64))
        model.add(Dense(self.env.ACTION_SPACE_SIZE, activation="linear"))

        model.compile(loss="mse",
                      optimizer=Adam(lr=0.001),
                      metrics=["accuracy"])

        return model

    def act(self, observation, reward, done):
        """
        Method for making appropriate action

        Input:
            observation: np.array
            reward:
            done: boolean
        """
        pass
