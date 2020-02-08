import gym

class HaroldReach(gym.Env):
    def __init__(self):
        print("Initialised")

    def step(self):
        print("step")

    def reset(self):
        print('reset')
