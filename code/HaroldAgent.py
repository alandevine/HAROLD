#!/usr/bin/python3

import gym
import numpy as np
from keras.models import load_model
from ReplayBuffer import ReplayBuffer, build_dqn
from gym.wrappers import FlattenObservation, FilterObservation

"""
TODO:
    * Comment Code
    * Implement some form of training history, e.g.
        + Rewards given,
        + Score given,
        + epsilon value,
        + etc
"""


class HaroldAgent(object):

    def __init__(
                self,
                alpha,                   # Learning Rate
                gamma,                   # Discount Factor
                n_actions,               # Number of actions available in the
                                         # envirnoment
                epsilon,                 # Random Factor
                batch_size,
                input_dims,
                epsilon_dec=0.9999,      # Rate at which the epsilon value
                                         # decreases
                epsilon_min=0.1,         # Value at which epsilon stops
                                         # decrementing
                memory_size=1000000,     # Maximum size of alotted memory
                file_name="harold_dqn",  # File name for the model

                # Below values are subject to change
                n_epochs=200,            # Number of epochs to be completed
                n_episodes=80,           # Number of episodes per epoch
                n_time_steps=50,         # Number of choices made by agent
                K=4                      # Number of random future states
            ):

        self.action_space = [i for i in range(n_actions)]
        self.n_actions = n_actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_dec = epsilon_dec
        self.epsilon_min = epsilon_min
        self.batch_size = batch_size
        self.model_file = file_name
        self.n_time_steps = n_time_steps

        self.env = gym.make('HaroldReach-v0')
        self.n_epochs = n_epochs
        self.n_episodes = n_episodes
        self.K = K

        self.memory = ReplayBuffer(memory_size,
                                   input_dims,
                                   n_actions,
                                   discrete=False)

        self.q_eval = build_dqn(alpha, n_actions, input_dims, 256, 256)

    def save(self, state, action, reward, new_state, done):
        """Interface between Agent and ReplayBuffer"""
        self.memory.store_transition(state, action, reward, new_state, done)

    def act(self, state):
        state = np.asarray(state)
        state = state[np.newaxis, :]

        # Generate random value to see if we will take a random action
        random_epsilon = np.random.random()

        if random_epsilon < self.epsilon:
            # Select random action
            action = self.env.action_space.sample()
        else:
            actions = self.q_eval.predict(state)[0]
            self.epsilon *= self.epsilon_dec
            # Select an action of the highest value
            action = actions[np.argmax(actions)]

        return action

    def learn(self):
        """Method that contains learning algorithms"""

        if self.memory.memory_counter < self.batch_size:
            return

        return_vals = self.memory.sample_buffer(-1)
        state, action, reward, new_state, done = return_vals

        action_values = np.array(action, dtype=np.int8)
        action_indices = int(np.dot(action.T, action_values))

        q_eval = self.q_eval.predict(state.T)
        q_next = self.q_eval.predict(new_state.T)

        q_target = q_eval.copy()

        batch_index = np.arange(self.batch_size, dtype=np.int32)

        # DeepQLearning Algorithm
        q_target[batch_index, action_indices] = (reward
                                                 + self.gamma
                                                 * np.max(q_next, axis=1)
                                                 * int(done))

        _ = self.q_eval.fit(state.T, q_target, verbose=0)

        # Decrement epsilon value by the gradient decent value
        if self.epsilon > self.epsilon_min:
            self.epsilon = self.epsilon * self.epsilon_dec

    def train(self):
        """Method for training the Network"""

        for epoch in range(self.n_epochs):
            for episode in range(self.n_episodes):

                done = False
                score = 0

                episode_experience = []

                # Reset the environment to it's initial state
                observation = self.env.reset()
                observation = FlattenObservation(
                                    FilterObservation(
                                            observation,
                                            ['observation',
                                             'achieved_goal',
                                             'desired_goal']
                                    )
                              )

                # Because we are not working with a continous action space,
                # we are limiting ourselfs to a finite number of timesteps
                # per episode, other wise the below for loop would be replaced
                # with `while not done:`

                for _ in range(self.n_time_steps):

                    self.env.render()
                    action = self.act(observation['observation'])
                    print(action)
                    new_observation, reward, done, info = self.env.step(action)

                    score += reward

                    episode_experience.append((observation['observation'],
                                               action,
                                               reward,
                                               new_observation['observation'],
                                               done))

                    self.save(np.asarray(observation['observation']),
                              action,
                              reward,
                              new_observation['observation'],
                              done)

                    observation = new_observation
                    self.learn()

                    # break if we finish the environment
                    if done is True:
                        break

                # HER Algorithm
                for t in range(len(episode_experience)):
                    for _ in range(self.K):
                        future = np.random.randint(t, len(episode_experience))
                        goal = episode_experience[future][3]
                        state = episode_experience[t][0]
                        action = episode_experience[t][1]
                        next_state = episode_experience[t][3]
                        done = np.array_equal(next_state, goal)
                        reward = 0 if done else -1

                        self.save(state, action, reward, next_state, done)

            # save model every 5 epochs
            # this is an arbitrary number and will change
            if epoch % 10 == 0 and epoch > 0:
                self.save_model

    def save_model(self):
        self.q_eval.save(self.model_file)

    def load_model(self):
        self.q_eval = load_model(self.model_file)
