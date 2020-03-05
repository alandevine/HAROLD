import pybullet as p
import time
import pybullet_data

# physicsClient = p.connect(p.DIRECT) for non-graphical version
physicsClient = p.connect(p.GUI)
p.setGravity(0,0,-9.81)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# Load ground plane into environment
planeID = p.loadURDF("plane.urdf")

startPos = [0,0,3]
startOrn = p.getQuaternionFromEuler([0,0,0])

# Load arm into environment
HaroldID = p.loadURDF("robot.xml", startPos, startOrn)
while True:
    p.stepSimulation()
    time.sleep(1./240.)
