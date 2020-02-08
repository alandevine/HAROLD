#!/usr/bin/python3

import numpy as np

from keras.layers import Dense, Activation
from keras.models import Sequential
from keras.optimizers import Adam


class ReplayBuffer(object):
    def __init__(
                self,
                max_size,       #
                input_shape,    #
                n_actions,      # Number of actions availabe to Agent
                discrete=False  #
            ):

        self.memory_size = max_size
        self.input_shape = input_shape
        self.n_actions = n_actions
        self.discrete = discrete

        self.state_memory = np.zeros((self.memory_size, self.input_shape))
        self.new_state_memory = np.zeros((self.memory_size, self.input_shape))

        self.action_memory = np.zeros((self.memory_size, self.n_actions))
        self.reward_memory = np.zeros(self.memory_size)
        self.terminal_memory = np.zeros(self.memory_size, dtype=np.float32)

        self.memory_counter = 0

    def store_transition(self, state, action, reward, new_state, done):

        """Method for updating numpy arrays after episode
        Kwargs:
            state     |
            action    |
            reward    |
            new_state |
            done      | Boolean Value
        """

        index = self.memory_counter % self.memory_size
        self.state_memory[index] = state
        self.new_state_memory[index] = new_state
        self.reward_memory[index] = reward
        self.terminal_memory[index] = 1 - int(done)

        if self.discrete:
            actions = np.zeros(self.action_memory.shape[1])
            actions[action] = 1.0
            self.action_memory[index] = actions

        else:
            self.action_memory[index] = action

        self.memory_counter += 1

    def sample_buffer(self, batch_size):
        max_memory = min(self.memory_counter, self.memory_size)
        batch = np.random.choice(max_memory, batch_size)

        states = self.state_memory[batch]
        new_states = self.new_state_memory[batch]
        rewards = self.reward_memory[batch]
        actions = self.action_memory[batch]
        terminal = self.terminal_memory[batch]

        return states, actions, rewards, new_states, terminal


def build_dqn(learning_rate, n_actions, input_dims, fc1_dims, fc2_dims):

    """Function to create a deep q network"""

    model = Sequential([
                Dense(fc1_dims, input_shape=[input_dims, ]),
                Activation("relu"),
                Dense(fc2_dims),
                Activation("relu"),
                Dense(n_actions)
        ])

    model = compile(optimizer=Adam(lr=learning_rate), loss="mse")

    return model
