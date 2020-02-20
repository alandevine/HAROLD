import gym
import envs

env= gym.make('HaroldReach-v0')

observation = env.reset()
while True:
    env.render()
    action = [0.0] * 7
    observation, reward, done, info = env.step(action)
