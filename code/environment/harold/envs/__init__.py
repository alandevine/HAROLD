from gym.envs.registration import register

register(
    id='HaroldReach-v0',
    entry_point='envs.harold_reach_env:HaroldReach',
    max_episode_steps=200
)

register(
    id='HaroldPickPlace-v0',
    entry_point='envs.harold_pick_and_place_env:HaroldPickPlace',
    max_episode_steps=200
)

