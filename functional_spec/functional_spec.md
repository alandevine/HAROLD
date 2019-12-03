0. Table of contents
1. Introduction
1.1 Overview
1.2 Business Context
1.3 Glossary
2. General Description
2.1 Product / System Functions
2.2 User Characteristics and Objectives
2.3 Operational Scenarios
2.4 Constraints
3. Functional Requirements
4. System Architecture
5. High-Level Design
6. Preliminary Schedule
7. Appendices


## 1. Introduction

### 1.1 Overview
H.A.R.O.L.D is a robotic arm which will be trained using a combination of *Reinforcement Learning*, *H.E.R*, and *D.D.P.G*, which allows us to create a functional and accurate robotic arm, which does not require a *P.I.D Controller* to move smoothly. The aim of this project is to train H.A.R.O.L.D to be able to grab, lift and reposition a given object to a specified location.

We will be using 2 HIMAX cameras, one mounted externally and on mounted on the arm, in order to give H.A.R.O.L.D greater positional awareness as well as being able to locate the object it wants to pick up in relation to itself.

Given enough time, we also plan to implement a *GUI* which allows the user to select an object, which will be classified by a pre-trained network, for H.A.R.O.L.D to pick up and reposition.

### 1.2 Business Context

Robotics play a huge role in the manufacturing industry which allows much of the manual labor to be automated, current implementations are inflexible as they require static environments, and if something is off, the system cannot account for it and fails. 

Current 

By making use of *machine learning* and *neural networks*, we can both remove the aforementioned need for specialized training and the strict rules which current implementations must abide by.

### 1.3 Glossary

1. Reinforcemnet Learning
   - A form of machine learning which doesn't require any datasets.
2. H.E.R (Hindsight Experience Replay)
   - A method of simulating artificial data by "pretending" that the goal was different to the goal when training was actually running.<sub>[[arXiv:1707.01495]](https://arxiv.org/pdf/1707.01495.pdf)[cs.LG]</sub>
3. D.D.P.G (Deep Deterministic Policy Gradient)
4. P.I.D Controller
   - An instrument used in industrial control applications to regulate temperature, flow, pressure, speed and other process variables. PID (proportional integral derivative) controllers use a control loop feedback mechanism to control process variables and are the most accurate and stable controller.<sub>[]()</sub>
5. Machine Learning
   - The scientific study of algorithms and statistical models that computer systems use to preform a specific task without explicit instructions.
6. Neural Network
   - A collection of nodes connected by synapses which recieve and process signals to complete a task.

## 2. General Description

### 2.1 Product / System Functions


## 3. Functional Requirements

### 3.1 Arm moves towards object

##### Description

The robot arm must be able to move towards the object to pick up, such that the clamp can grasp said object.

##### Criticality

This is an essential step in picking up an object, since if the object is out of range it cannot be held by the clamp.

##### Technical issues

The main issue is whether we can get the network to train sufficiently so that it can move to the object accurately and consistently.

##### Dependencies on other requirements

This depends on the *classifier* being able to recognise the object and create a bounding box around it.

### 3.2 Clamp grasps object

##### Description

The clamp mounted on the arm will close such that it grasps any object which is positioned between the clamp.

##### Criticality

It is important for the clamp to be able to grasp the object firmly so as not to drop it while trying to reposition it

##### Technical issues

It's important issue for us to consider the weight of the object in relation to the strength of the servos controlling the arm, as it will not be able to lift the object if it can't grasp it firmly enough.

##### Dependencies on other requirements

This stage depends heavily on the arm moving to the object, since the object cannot be held if it's not in range of the arm.

### 3.3 Moving the object to a designated space

##### Description

Once the object is held, the arm will lift it, and move the object to an area with a *DM* printed onto a page, designating where the object will be placed.

##### Criticality

In order for this arm to be used in an industrial setting, it must be able to consistently and accurately move objects to their desired location.

##### Technical issues

Again, it's important for us to make sure the object being moved is not too heavy for the servos to be able to lift and move.

##### Dependencies of other requirements

This step is dependent on both the arm being able to grasp the object well, and also on the *classifier* being able to detect and locate the *DM* consistently.

### 3.4 Classifier

##### Description

A *Neural Network* able to recognise and label an object, allowing the arm to locate specific objects and locations.

##### Criticality

This is a very important part of the project as the arm will not be able to detect any objects without it.  Since this is such an important part which requires a lot of training and a large dataset to develop, we have decided to use a pre-trained network.

##### Technical issues

Most *CCN*s are dependent on lighting conditions, but since it won't be our own network, we wont know the limitations without first select and then test it.

