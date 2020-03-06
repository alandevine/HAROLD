from .. import harold_env
import os
from gym import utils


MODEL_XML_PATH = '/home/fuentes/programming/harold/code/environment/assets/xml/pick_and_place.xml'


class HaroldPickPlace(harold_env.HaroldEnv, utils.EzPickle):
    """
    Environment Class for picking up and placing an object
    """

    def __init__(self, reward_type='sparse'):

        initial_qpos = {
        }

        harold_env.HaroldEnv.__init__(
                self, MODEL_XML_PATH,
                has_object=True,
                block_gripper=False,
                n_substeps=20,
                target_in_the_air=True,
                target_offset=0.0,
                obj_range=250.0,
                target_range=200.0,
                distance_threshold=20,
                initial_qpos=initial_qpos,
                reward_type=reward_type,
                n_actions=8
        )

        utils.EzPickle.__init__(self)
