# H.A.R.O.L.D
## Harold - Accurately - Repositions - Optically - Located - Doohickeys
=====

### Installation

In order to use the Mujoco physics engine, you need to have a license, so instead use `pip install pybullet` which is an open-source alternative for use with OpenAI gym

After this, use `pip install -r requirements.txt` to install most of the requirements for the simulation to work

Lastly, there a number of modules which we install from local directories,  to do this, leave the this directory and use `git clone https://github.com/openai/gym && cd gym && pip install -e .` which will install the OpenAI gym environment
We then need to install our custom environments for OpenAI gym to simulate. go back to the repo directory the use `cd code/pybullet/harold_bullet && pip install -e .` Which will install the pybullet version of our custom environment.