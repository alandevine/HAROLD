import pybullet as p
import time
import pybullet_data

import cloudpickle

from stable_baselines import HER, DDPG
from stable_baselines.common.policies import MlpPolicy

import numpy as np

from random import randint


def getScore(goal, pos):
    score = (pos[0] - goal[0])**2 + (pos[1] - goal[1])**2 + (pos[2]-goal[2])**2
    return score ** 0.5

def main():
    model_class = DDPG

    

    p.connect(p.GUI)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0,0,-9.8)

    for i in range(1000):

        plane = p.loadURDF("plane.urdf")
        arm = p.loadURDF("robot.xml", useFixedBase=True, flags=p.URDF_USE_SELF_COLLISION)
        goalPos = [randint(40,60),randint(-30,30),randint(2,40)]
        goal = p.loadURDF("goal.xml", goalPos,useFixedBase=True)

        jointIDs = []  
        handJoints = []
        paramIDs = []

        for i in range(4):
            # Changes all joint physics properties to be the same
            p.changeDynamics(arm, i, linearDamping=0, angularDamping=0)
            info = p.getJointInfo(arm, i)
            #print(info)
            jointName = info[1]
            jointType = info[2]
            if (jointType == p.JOINT_REVOLUTE):
                jointIDs.append(i)
                paramIDs.append(p.addUserDebugParameter(jointName.decode("utf-8"), -1, 1, 0))

        # Don't render every frame of the simulation
        skip_cam_frames = 10

        for j in range(1000):
        
            p.stepSimulation()
            for i in range(len(paramIDs)):
                if i in handJoints:
                    p.resetJointState(handJoints[i])
                else:
                    c = paramIDs[i]
                targetPos = p.readUserDebugParameter(c)
                p.setJointMotorControl2(arm, jointIDs[i], p.POSITION_CONTROL, targetPos, force=5 * 240.)
            skip_cam_frames -= 1
            if (skip_cam_frames<0):
                p.getCameraImage(320, 200, renderer=p.ER_BULLET_HARDWARE_OPENGL)
                skip_cam_frames = 10
            time.sleep(1./240.)
            hand_pos = p.getLinkState(arm, 4)[0]
            score = getScore(goalPos, hand_pos)
            print(score)

        p.resetSimulation()

if __name__ == "__main__":
    main()
