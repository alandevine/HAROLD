from .. import harold_env
import os
from gym import utils


MODEL_XML_PATH = '/home/fuentes/programming/harold/code/environment/assets/xml/reach.xml'


class HaroldReach(harold_env.HaroldEnv, utils.EzPickle):
    """
    Environment Class for reaching for an object
    """

    def __init__(self, reward_type='sparse'):

        initial_qpos = {
        }

        harold_env.HaroldEnv.__init__(
                self, MODEL_XML_PATH,
                has_object=False,
                block_gripper=True,
                n_substeps=20,
                target_in_the_air=True,
                target_offset=0.0,
                obj_range=250.0,
                target_range=200.0,
                distance_threshold=1,
                initial_qpos=initial_qpos,
                reward_type=reward_type,
                n_actions=7
        )

        utils.EzPickle.__init__(self)
