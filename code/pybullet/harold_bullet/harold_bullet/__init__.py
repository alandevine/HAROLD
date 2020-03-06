from gym.envs.registration import register

register(
    id='haroldReachBullet-v0',
    entry_point='harold_bullet.envs:HaroldBulletEnv',
)