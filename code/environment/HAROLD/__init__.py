from gym.envs.registration import register

register(
    id="HAROLD-v0",
    entry_point="HAROLD.envs:HaroldEnv"
)

register(
    id="harold-extrahard-v0",
    entry_point="HAROLD.envs:HaroldExtraHardEnv",
)
