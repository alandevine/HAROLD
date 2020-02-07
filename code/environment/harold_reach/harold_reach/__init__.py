from harold_reach.envs.registration import register

register(
    id='harold-reach-v0',
    entry_point='harold_reach.envs:HaroldReach',
)
register(
    id='harold-extrahard-v0',
    entry_point='harold_reach.envs:FooExtraHardEnv',
)
