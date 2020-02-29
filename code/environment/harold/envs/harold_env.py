import os
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

    def __init__(
            self, model_path, has_object, block_gripper, n_substeps,
            target_in_the_air, target_offset, obj_range, target_range,
            distance_threshold, initial_qpos, reward_type, n_actions
    ):
        '''
        Initialise a new Harold Environment
        
        __________
        Args:
            model_path(String)          : Path to xml environment to load
            has_object(Bool)            : State whether there is an object to load
            block_gripper(Bool)         : State if the grippers can move or not
            n_substeps(Int)             : Number of substeps to carry out for each step
            target_in_the_air(Bool)     : State if the target can be in the air
            target_offset(Float)        : Offset of the target
            obj_range(Float)            : Range of uniform distribution for sampling the initial object positions
            target_range(Float)         : Range of unifrom distribution for sampling the initial target position
            distance_threshold(Float)   : How close the achieved goal must be to consider it successful
            initial_qpos(Dict)          : Dictionary containing initial position of joints
            reward_type(String)         : Which reward type to use (dense or sparse)
        '''

        self.has_object = has_object
        self.block_gripper = block_gripper
        self.target_in_the_air = target_in_the_air
        self.target_offset = target_offset
        self.obj_range = obj_range
        self.target_range = target_range
        self.distance_threshold = distance_threshold
        self.reward_type = reward_type
        self.n_actions = n_actions

        super(HaroldEnv, self).__init__(
                model_path=model_path, initial_qpos=initial_qpos, n_actions=n_actions, n_substeps=n_substeps
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
            self.sim.data.set_joint_qpos('robot0:servo_gear_b', 0.)
            self.sim.data.set_joint_qpos('robot1:servo_gear_a', 0.)
            self.sim.data.set_joint_qpos('robot1:finger_right', 0.)
            self.sim.data.set_joint_qpos('robot1:finger_left',  0.)
            self.sim.data.set_joint_qpos('robot1:pivot_arm_a',  0.)
            self.sim.data.set_joint_qpos('robot1:pivot_arm_b',  0.)
            self.sim.forward()

    def _set_action(self, action):
        '''
        Sets the action to apply to the simulation
        '''
        assert action.shape == (self.n_actions,)
        # Ensure the action doesn't change outside of this scope
        action = action.copy()
        pos_ctrl, gripper_ctrl = action[:3], action[3]

        # Limit the maximum change in position
        pos_ctrl *= 20
        # Fix roation of the hand, expressed as a quaterion
        rot_ctrl = action[4:]
        gripper_ctrl = np.array([gripper_ctrl])
        assert gripper_ctrl.shape == (1,)
        if self.block_gripper:
            gripper_ctrl = [0.0]
        action = np.concatenate([pos_ctrl, rot_ctrl, gripper_ctrl])

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
            object_rel_pos = object_pos - grip_pos
            object_velp -= grip_velp
        else:
            object_pos = object_rot = object_velp = object_velr = object_rel_pos = np.zeros(3)
        gripper_state = robot_qpos[-2:]
        # Change to a scalar if the gripper is symmetric
        gripper_vel = robot_qvel[-2:] * dt

        if not self.has_object:
            achieved_goal = np.squeeze(self.sim.data.get_site_xpos('robot0:gripper').copy())
        else:
            achieved_goal = np.squeeze(object_pos.copy())
        obs = np.concatenate([
            grip_pos, object_pos.ravel(), object_rel_pos.ravel(),
            gripper_state, object_rot.ravel(), object_velp.ravel(),
            object_velr.ravel(), grip_velp, gripper_vel
        ])

        return {
            'observation': obs.copy(),
            'achieved_goal': achieved_goal.copy(),
            'desired_goal': self.goal.copy()
        }

    def _viewer_setup(self):
        '''
        Setup viewer window for rendering environment
        '''
        body_id = self.sim.model.body_name2id('robot0:hand')
        lookat = self.sim.data.body_xpos[body_id]
        for idx, value in enumerate(lookat):
            self.viewer.cam.lookat[idx] = value
        self.viewer.cam.distance = 1000
        self.viewer.cam.azimuth = 450.
        self.viewer.cam.elevation = 0.

    def _render_callback(self):
        '''
        Visualise Target
        '''
        site_id = self.sim.model.site_name2id('target0')
        self.sim.model.site_pos[site_id] = self.goal
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
                object_xpos = self.initial_gripper_xpos[:2] + self.np_random.uniform(-self.obj_range, self.obj_range, size=2)
            object_qpos = self.sim.data.get_joint_qpos('object0:joint')
            assert object_qpos.shape == (7,)
            object_qpos[:2] = object_xpos
            self.sim.data.set_joint_qpos('object0:joint', object_qpos)

        self.sim.forward()
        obs = self._get_obs()
        return obs

    def _sample_goal(self):
        if self.has_object:
            goal = self.initial_gripper_xpos[:3] + self.np_random.unifrom(-self.target_range, self.target_range, size=3)
            goal += self.target_offset
            goal[2] = self.height_offset
            if self.target_int_the_air and self.np_random_uniform() < 0.5:
                goal[2] += self.np_random.uniform(0, 0.45)
        else:
            goal = self.initial_gripper_xpos[:3] + self.np_random.uniform(-self.target_range, self.target_range, size=3)
        return goal.copy()

    def _is_success(self, achieved_goal, desired_goal):
        d = goal_distance(achieved_goal, desired_goal)
        return (d < self.distance_threshold).astype(np.float32)

    def _env_setup(self, initial_qpos):
        for name in initial_qpos:
            self.sim.data.set_joint_qpos(name, initial_qpos[name])
        utils.reset_mocap_welds(self.sim)
        self.sim.forward()

        # Move gripper into position
        gripper_target = np.array([0.0, 0.0, 0.0]) + self.sim.data.get_site_xpos('robot0:gripper')
        gripper_rotation = np.array([1., 0., 0., 0.]) 
        self.sim.data.set_mocap_pos('robot0:mocap', gripper_target)
        self.sim.data.set_mocap_quat('robot0:mocap', gripper_rotation)
        for _ in range(10):
            self.sim.step()

        # Extract information for sampling goals
        self.initial_gripper_xpos = self.sim.data.get_site_xpos('robot0:gripper').copy()
        if self.has_object:
            self.height_offset = self.sim.data.get_site_xpos('object0')[2]

    def render(self, mode='human', width=500, height=500):
        return super(HaroldEnv, self).render(mode, width, height)
