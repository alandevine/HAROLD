
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


### 1.2 Business Context

Robotics play a huge role in the manufacturing industry which allows much of the manual labor to be automated, current implementations are inflexible as they require static environments, and if something is off, the system cannot account for it and fails. 

Current 

By making use of machine learning and neural networks, we can both remove the aforementioned need for specialized training and the strict rules which current implementations must abide by.


---
garbage
--

H.A.R.O.L.D will be a Computer Vision driven robotic arm designed for repositioning generic objects in a given area. He will be built on a Convolutional Neural Network and will make use of the Movidius Neural Compute Stick to accelerate the Network. 

These modifications will be in the form of 2 HIMAX cameras. The HIMAX cameras will be located on the body and looking perpendicular to the surface of operation for greater positional awareness, by allowing it to visually locate itself and the object in question.

The arm will be trained using a combination of Reinforment Learning and H.E.R. Training will be done via a combination of simulated learning enviroments to remove external variables, optimizing traing, and 

A Convolutional Neural Network is a type of network which is specialised to run inference on image data, allowing the network to label specific objects in an image or frame of a video. We plan to use this to label both the object and the arm itself in order to orientate and pickup the object accurately and place it down in a specified location.