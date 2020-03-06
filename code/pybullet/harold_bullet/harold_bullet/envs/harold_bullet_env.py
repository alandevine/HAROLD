import gym
from gym import error, spaces, utils
from gym.utils import seeding

import pybullet as p
import pybullet_data

import numpy as np

from random import randint

class HaroldBulletEnv(gym.GoalEnv):
    metadata = {'render.modes': ['human', 'rgb_array']}


    def __init__(self):
        self._observation = []
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=-100, high=100, shape=(10,))
        self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        self._seed()
    

    def _step(self, action):
        """
        Step through the simulation after applying the selected actions,
        and returns the observation, reward and done flag
        """

        self._assign_move(action)
        p.stepSimulation()
        self._observation = self._compute_observation()
        reward = self._compute_reward()
        done = self._compute_done()

        return self._observation, reward, done, {}
    

    def _assign_move(self, action):
        """
        Selects a velicty for each joint from the Q-Table
        """

        dv = 0.1
        # Choose an action for each joint
        for i in range(action):
            # Q-table of joint velocities
            print(action)
            deltav = [-10.*dv, -5.*dv, -2.*dv, -0.1*dv, 0, 0.1*dv, 2.*dv, 5.*dv, 10.*dv][action[0][i]]
            vt = self.vt + deltav
            self.vt = vt
            # pyBullet method for controlling joints
            p.setJointMotorControl2(bodyUniqueId=self.botId,
                                    jointIndex=i,
                                    controlMode=p.VELOCITY_CONTROL,
                                    targetVelocity=action[i])
    

    def _compute_observation(self):
        """
        Returns an array containing joint positions, goal position, and hand position
        """

        observation = []

        jointValues = []

        for i in range(4):
            info = p.getJointInfo(bodyUniqueId=self.botId,
                                  jointIndex=i)
            observation.append(info[3])
        
        #observation.append(jointValues)
        observation += self.goalPos

        handPos = list(p.getLinkState(bodyUniqueId=self.botId,
                                 linkIndex=4)[0])
        
        observation += handPos

        return np.reshape(observation, (10,))
    

    def _compute_reward(self):
        """
        Returns the distance between the goal and the hand location
        """
        
        handPos = list(p.getLinkState(bodyUniqueId=self.botId,
                                 linkIndex=4)[0])
        
        score = ((handPos[0] - self.goalPos[0])**2 + (handPos[1] - self.goalPos[1])**2 + (handPos[2] - self.goalPos[2])**2) ** 0.5

        return score

    
    def _compute_done(self):
        """
        Returns whether the arm is within a certain threshold to the goal
        """

        return self._compute_reward() >= 5

    
    def _get_goal(self):
        """
        Sets the position for the goal within a certain range
        """

        goalPos = [randint(40,60),randint(-30,30),randint(2,40)]
        return goalPos


    def _reset(self):
        """
        Reset the environment
        """

        self.vt = 0
        self.vd = 0
        
        p.resetSimulation()
        p.setGravity(0,0,-10)
        p.setTimeStep(0.01)

        planeId = p.loadURDF("plane.urdf")
        self.botId = p.loadURDF("robot.xml")

        self.goalPos = self._get_goal()
        goalId = p.loadURDF("goal.xml",self.goalPos)

        self._observation = self._compute_observation()
        return self._observation

    
    def _render(self, mode='human', close=False):
        """
        Handled by pybullet so pass
        """
        pass

    
    def _seed(self, seed=None):
        """
        Returns a random seed for the simulation
        """

        self.np_random, seed = seeding.np_random(seed)
        return [seed]