#!/bin/bash

sudo apt install python3-venv



# Setup mujoco engine
wget https://www.roboti.us/download/mujoco200_linux.zip
mkdir ~/.mujoco
mv mujoco_linux.zip ~/.mujoco
unzip mujoco_linux.zip && rm mujoco_linux.zip
mv mujoco200_linux mujoco200
cp mjkey.txt ~/.mujoco && cp mjkey.txt ~/.mujoco/mujoco200/bin

# Setup OpenAI Gym
mkdir ~/programming && cd programming
mkdir venv
python3 -m venv venv/harold
. venv/harold/bin/activate
git clone https://github.com/openai/gym && cd gym
pip install -e .

# Setup Mujoco-py
cd ~/programming
git clone https://github.com/openai/mujoco-py && cd mujoco-py
