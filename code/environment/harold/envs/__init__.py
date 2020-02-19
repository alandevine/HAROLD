from gym.envs.registration import register

register(
    id='HaroldReach-v0',
    entry_point='envs.harold_reach_env:HaroldReach'
)

