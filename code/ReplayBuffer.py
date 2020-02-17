#!/usr/bin/python3

import numpy as np

from keras.layers import Dense, Activation
from keras.models import Sequential
from keras.optimizers import Adam


class ReplayBuffer(object):

    """Class for storing transitions from training"""

    def __init__(
                self,
                memory_size,    #
                input_shape,    # Shape of the matrix
                n_actions,      # Number of actions availabe to Agent
                discrete=False  # Boolean that corisponds to discrete
                                # action spaces
            ):

        self.memory_size = memory_size
        self.input_shape = input_shape
        self.n_actions = n_actions
        self.discrete = discrete

        self.state_memory = np.zeros((self.memory_size, self.input_shape))
        self.new_state_memory = np.zeros((self.memory_size, self.input_shape))

        dtype = np.int8 if self.discrete else np.float32

        self.action_memory = np.zeros(
                    (self.memory_size, self.n_actions), dtype=dtype)

        self.reward_memory = np.zeros(self.memory_size)
        self.terminal_memory = np.zeros(self.memory_size, dtype=np.float32)

        self.memory_counter = 0

    def store_transition(self, state, action, reward, new_state, done):

        """Method for updating numpy arrays after episode
        Kwargs:
            state     |
            action    |
            reward    |
            new_state | Numpy Array
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

    def random_sample(self, batch_size):
        max_memory = min(self.memory_counter, self.memory_size)
        batch = np.random.choice(max_memory, batch_size)

        states = self.state_memory[batch]
        new_states = self.new_state_memory[batch]
        rewards = self.reward_memory[batch]
        actions = self.action_memory[batch]
        terminal = self.terminal_memory[batch]

        return states, actions, rewards, new_states, terminal

    def sample_buffer(self, index):
        states = self.state_memory[index]
        new_states = self.new_state_memory[index]
        rewards = self.reward_memory[index]
        actions = self.action_memory[index]
        terminal = self.terminal_memory[index]

        return states, actions, rewards, new_states, terminal


def build_dqn(learning_rate, n_actions, input_dims, fc1_dims, fc2_dims):

    """Function to create a deep q network
    Makes use of a Rectified Linear Unit approach as opposed to a sigmoid
    function for modifying branch weights
    """

    model = Sequential([
                Dense(fc1_dims, input_shape=[input_dims, ]),
                Activation("relu"),
                Dense(fc2_dims),
                Activation("relu"),
                Dense(n_actions)
        ])

    model = compile(optimizer=Adam(lr=learning_rate), loss="mse")

    return model
