#!/usr/bin/python3

import numpy as np

from keras.models import load_model
from ReplayBuffer import ReplayBuffer, build_dqn
from environment.harold_reach.envs.harold_reach_env.harold_reach import HaroldReach

"""
TODO:
    * Implement Hindsight Experince Replay in the learn method
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
                alpha,              # Learning Rate
                gamma,              # Discount Factor
                n_actions,
                epsilon,            # Random Factor
                batch_size,
                input_dims,
                epsilon_dec=0.996,  # Rate at which our epsilon value decreases
                epsilon_min=0.1,    # Value at which epsilon stops decrementing
                memory_size=1000000,
                file_name="harold_dqn",
                n_epochs=200,       # Collection of episodes
                n_episodes=80
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

        self.env = HaroldReach()
        self.n_epochs = n_epochs
        self.n_episodes = n_episodes

        self.memory = ReplayBuffer(memory_size,
                                   input_dims,
                                   n_actions,
                                   discrete=True)

        self.q_eval = build_dqn(alpha, n_actions, input_dims, 256, 256)

    def save(self, state, action, reward, new_state, done):
        """Interface between Agent and ReplayBuffer"""
        self.memory.store_transition(state, action, reward, new_state, done)

    def act(self, state):
        state = state[np.newaxis, :]

        # Generate random value to see if we will take a random action
        random_epsilon = np.random.random()

        if random_epsilon < self.epsilon:
            # Select random action
            action = np.random.choice(self.action_space)
        else:
            actions = self.q_eval.predict(state)
            # Select an action of the highest value
            action = np.argmax(actions)

        return action

    def learn(self):
        """Method that contains learning algorithms"""
        if self.memory.memory_counter < self.batch_size:
            return

        return_vals = self.memory.sample_buffer(self.batch_size)
        state, action, reward, new_state, done = return_vals

        action_values = np.array(self.action, dtype=np.int8)
        action_indices = np.dot(action, action_values)

        q_eval = self.q_eval.predict(state)
        q_next = self.q_eval.predict(new_state)

        q_target = q_eval.copy()

        batch_index = np.arange(self.batch_size, dtype=np.int32)

        # DeepQLearning Algorithm
        q_target[batch_index, action_indices] = (reward
                                                 + self.gamma
                                                 * np.max(q_next, axis=1)
                                                 * done)

        _ = self.q_eval.fit(state, q_target, verbose=0)

        # Decrement epsilon value by the gradient decent value
        if self.epsilon > self.epsilon_min:
            self.epsilon = self.epsilon * self.epsilon_dec

    def train(self):
        """Method for training the Network"""

        for epoch in range(self.n_epochs):
            for episode in range(self.n_episodes):
                done = False
                score = 0
                observation = self.env.reset()

                # Because we are not working with a continous action space,
                # we are limiting ourselfs to a finite number of timesteps
                # per episode, other wise the below for loop would be replaced
                # with `while not done:`

                for _ in range(self.time_step):

                    action = self.act(observation)
                    new_observation, reward, done, info = self.env.step(action)

                    score += reward
                    self.save(observation,
                              action,
                              reward,
                              new_observation,
                              done)

                    # break if we finish the environment
                    if done is True:
                        break

            # save model every 5 epochs
            # this is an arbitrary number and will change
            if epoch % 10 == 0 and epoch > 0:
                self.save_model

    def save_model(self):
        self.q_eval.save(self.model_file)

    def load_model(self):
        self.q_eval = load_model(self.model_file)
