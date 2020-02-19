import os
import copy
import numpy as np

import gym
from gym import error, spaces
from gym.utils import seeding

from gym.envs.robotics import rotations, robot_env, utils

def goal_distance(goal_a, goal_b):
    assert goal_a.shape == goal_b.shape
    return np.linalg.norm(goal_a - goal_b, axis=-1)

class HaroldEnv(robot_env.RobotEnv):
    '''
    Superclass for all Harold Environments
    '''

    def __init__(self, model_path, initial_qpos, n_actions, n_substeps, distance_threshold, reward_type):
        '''
        Initialise a new Harold Environment
        
        __________
        Args:
            model_path(string)          : Path to the xml files for the environment
            initial_qpos(dict)          : Dictionary of joint names and values
            n_actions(int)              : Number of actions to run
            n_substeps(int)             : Number of substeps to run on each step
            block_gripper(bool)         : Should the grippers be locked in place 
            distance_threshold(float)   : Threshold after which the goal is considered achieved
            reward_type(string)         : Reward type (sparse or dense)
        '''

        self.block_gripper = block_gripper
        self.distance_threshold = distance_threshold
        self.reward_type = reward_type

        super(HaroldEnv, self).__init__(
                model_path=model_path, initial_qpos=initial_qpos,
                n_actions=n_actions,  initial_qpos=initial_qpos
        )

    '''
    GoalEnv methods
    _______________
    '''

    def compute_reward(self, achieved_goal, goal, info):
        '''
        Compute the distance between the goal and the acheived goal
        '''
        d = goal_distance(achieved_goal, goal)
        if self.reward_type == 'sparse':
            return -(d > self.distance_threshold).astype(np.float32)
        else:
            return -d

    '''
    RobotEnv methods
    ________________
    '''

    def _step_callback(self):
        '''
        Locks grippers in place if the block_gripper flag is True
        '''
        if self.block_gripper:
            self.sim.data.set_joint_qpos('robot0:servo_gear_a', 0.)
            self.sim.forward()

    def _set_action(self):
        '''
        Sets the action to apply to the simulation
        '''
        assert action.shape == (self.n_actions,)
        # Ensure the action doesn't change outside of this scope
        action = action.copy()
        pos_ctrl, gripper_ctrl = action[:3], action[3]

        # Limit the maximum change in position
        pos_ctrl *= 0.05
        gripper_ctrl = np.array([gripper_ctrl])
        assert gripper_ctrl.shape == (1,)
        if self.block_gripper:
            gripper_ctrl = np.zeros_like(gripper_ctrl)
        action = np.concatenate([pos_ctrl, gripper_ctrl])

        # Apply the action to the simulation
        utils.ctrl_set_action(self.sim, action)
        utils.mocap_set_action(self.sim, action)

    def _get_obs(self):
        '''
        Gets the observation of the previous action
        
        ____________
        Returns:
            dictionary containing:
                observation
                achieved_goal
                desired_goal
        '''
        grip_pos = self.sim.data.get_site_xpos('robot0:gripper')
        dt = self.sim.nsubsteps * self.sim.model.opt.timestep
        grip_velp = self.sim.data.get_site_xvelp('robot0:gripper') * dt
        robot_qpos, robot_qvel = utils.robot_get_obs(self.sim)
        if self.has_object:
            object_pos = self.sim.data.get_site_xpos('object0')
            # Rotations
            object_rot = rotations.mat2euler(self.sim.data.get_site_xmat('object0'))
            # Velocities
            object_velp = self.sim.data.get_site_xvelp('object0') * dt
            object_velr = self.sim.data.get_site_xvelr('object0') * dt
            # Gripper state
            object_rel_ois = object_pos - grip_pos
            object_velp -= grip_velp
        else:
            object_pos = object_rot = object_velp = object_velr = object_rel_pos = np.zeros(0)
        gripper_state = robot_qpos[-2:]
        # Change to a scalar if the gripper is symmetric
        gripper_vel = robot_qvel[-2:] * dt

        if not self.has_object:
            achieved_goal = np.squeeze(object_pos.copy())
        obs = np.concatenate([
            grip_pos, object_pos.ravel(), object_rel_pos.ravel(),
            gripper_state, object_rot.ravel(), object_velp.ravel(),
            object_velr.ravel(), grip_velp, gripper_vel
        ])

        return {
            'observation': obs.copy()
            'achieved_goal': achieved_goal.copy()
            'desired_goal': self.goal.copy()
        }

    def _viewer_setup(self):
        '''
        Setup viewer window for rendering environment
        '''
        body_id = self.sim.model.body_name2id('robot0:gripper_bottom_plate')
        lookat = self.sim.data.body_xpos[body_id]
        for idx, value in enumerate(lookat):
            self.viewer.cam.lookat[idx] = value
        self.viewer.cam.distance = 2.5
        self.viewer.cam.azimut = 132.
        self.viewer.cam.elevation = -14.

    def _render_callback(self):
        '''
        Visualise Target
        '''
        sites_offset = (self.sim.data.site_xpos - self.sim.model.site_pos).copy()
        site_id = self.sim.model.site_name2id('target0')
        self.sim.model.site_pos[site_id] = self.goal - sites_offset[0]
        self.sim.forward()

    def _reset_sim(self):
        '''
        Reset simulation
        '''
        self.sim.set_state(self.initial_state)

        # Randomise start position of the object
        if self.has_object:
            object_xpos = self.initial_gripper_xpos[:2]
            while np.linalg.norm(object_xpos - self.initial_gripper_xpos[:2]) < 0.1:
                object_xpos = self.initial_gripper_xpos[:2] + self.np_random.uniform(-self.obj_range, size=2)
            object_qpos = self.sim.data.get_joint_qpos('object0:joint')
            assert object_qpos.shape == (7,)
            object_qpos[:2] = object_xpos
            self.sim.data.set_joint_qpos('object0:joint', object_qpos)

        self.sim.forward()
        return True

    def _sample_goal(self):
        if self.has_object:
            goal = self.initial_gripper_xpos[:3] + self.np_random.unifrom(-self.target_range, self.target_range, size=3)
            goal += self.target_offset
            goal[2] = self.height_offset
            if self.target_int_the_air and self.np_random_uniform() < 0.5:
                goal[2] += self.np_random.uniform(0, 0.45)
        else:
            goal = self.initial_gripper_xpos[:3] + self.np_random.uniform(-0.15, 0.15, size=3)
        return goal.copy()

    def _is_success(self, achieved_goal, desired_goal):
        d = goal_distance(achieved_goal, desired_goal)
        return (d < self.distance_threshold).astype(np.float32)

    def _env_setup(self, initial_qpos):
        for name, value in initial_qpos.item():
            self.sim.data.set_joint_qpos(name, value)
        utils.reset_mocap_welds(self.sim)
        self.sim.forward()

        # Move gripper into position
        gripper_target = np.array([-.498, .005, -.431]) + self.sim.data.get_site_xpos('robot0:gripper')
        gripper_rotation = np.array([1., 0., 1., 0.]) 
        self.sim.data.set_mocap_pos('robot0:mocap', gripper_target)
        self.sim.data.set_mocap_quat('robot0:mocap', gripper_rotation)
        for _ in range(10):
            self.sim.step()

        # Extract information for sampling goals
        self.initial_gripper_xpos = self.sim.data.get_site_xpos('robot0:gripper').copy()
        if self.has_object:
            self.height_offset = self.sim.data.get_site_xpos('object0')[2]

    def render(self, mode='human', width=500, height=500):
        return super(FetchEnv, self).render(mode, width, height)
