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
H.A.R.O.L.D is a robotic arm which will be trained using a combination of *Reinforcement Learning* and *H.E.R*, which allows us to create a functional and accurate robotic arm, which does not require a *P.I.D Controller* to move smoothly.

### 1.2 Business Context

Robotics play a huge role in the manufacturing industry which allows much of the manual labor to be automated, current implementations are inflexible as they require static environments, and if something is off, the system cannot account for it and fails. 

Current 

By making use of *machine learning* and *neural networks*, we can both remove the aforementioned need for specialized training and the strict rules which current implementations must abide by.

### 1.3 Glossary

1. Reinforcemnet Learning
   - A form of machine learning which doesn't require any datasets.
2. H.E.R (Hindsight Experience Replay)
   - A method of simulating artificial data by "pretending" that the goal was different to the goal when training was actually running.(arXiv:1707.01495 [cs.LG])
3. P.I.D Controller
   - An instrument used in industrial control applications to regulate temperature, flow, pressure, speed and other process variables. PID (proportional integral derivative) controllers use a control loop feedback mechanism to control process variables and are the most accurate and stable controller.
4. Machine Learning
   - The scientific study of algorithms and statistical models that computer systems use to preform a specific task without explicit instructions.
5. Neural Network
   - A collection of nodes connected by synapses which recieve and process signals to complete a task.
6. 

## 2. General Description

### 2.1 Product / System Functions


---
garbage
--

H.A.R.O.L.D will be a Computer Vision driven robotic arm designed for repositioning generic objects in a given area. He will be built on a Convolutional Neural Network and will make use of the Movidius Neural Compute Stick to accelerate the Network. 

These modifications will be in the form of 2 HIMAX cameras. The HIMAX cameras will be located on the body and looking perpendicular to the surface of operation for greater positional awareness, by allowing it to visually locate itself and the object in question.

The arm will be trained using a combination of Reinforment Learning and H.E.R. Training will be done via a combination of simulated learning enviroments to remove external variables, optimizing traing, and 

A Convolutional Neural Network is a type of network which is specialised to run inference on image data, allowing the network to label specific objects in an image or frame of a video. We plan to use this to label both the object and the arm itself in order to orientate and pickup the object accurately and place it down in a specified location.