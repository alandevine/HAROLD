import os
import gym
import mujoco_py

import numpy as np

from collections import OrderedDict
from gym import error, spaces
from gym.utils import seeding


class HaroldReach(gym.Env):
    """Environment Class for reaching for an object
    This will be broken up to a master class at some point
    """

    def __init__(self, model_path, frame_skip):
        self.model_path = model_path
        self.frame_skip = frame_skip

        self.sim = mujoco_py.load_model_from_path(self.model_path)
        self.data = self.sim.data
        self.viewer = None
        self._viewers = {}

        self.metadata = {
                "render.modes": ["human", "rgb_array", "depth_array"],
                "video.frames_per_second": int(np.round(1.0 / self.dt))
        }

        self.init_q_pos = self.sim.data.qpos.ravel().copy
        self.init_q_vel = self.sim.data.qpos.ravel().copy

        self._set_action_space()

        action = self.action_space.sample()
        observation, reward, done, info = self.step(action)

        assert not done

        self.seed()

        print("Initialised")

    # Training Methods

    def step(self):
        print("step")

    def reset(self):
        print('reset')

    # Methods for creating instance variables

    def _set_action_space(self):
        bounds = self.model.actuator_ctrlrange.copy
        low, high = bounds.T
        self.action_space = spaces.Box(low=low, high=high, dtype=np.float32)
        return self.action_space

    def _set_observation_space(self, observation):
        self.observation_space = self.convert_observation_to_space(observation)
        return self.observation_space

    def convert_observation_to_space(self, observation):
        if isinstance(observation, dict):
            space = spaces.Dict(OrderedDict([
                (key, self.convert_observation_to_space(value))
                for key, value in observation.items]))
        elif isinstance(observation, np.ndarray):
            low = np.full(observation.shape, -float('inf'))
            high = np.full(observation.shape, -float('inf'))
            space = spaces.Box(low, high, dtype=observation.dtype)

        else:
            raise NotImplementedError(type(observation), observation)

        return space

    def seed(self, seed="None"):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]
