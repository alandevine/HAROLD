import gym
import envs
import sys

env= gym.make(sys.argv[1])
env.step()
env.reset()
