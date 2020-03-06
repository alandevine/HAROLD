import gym

#from stable_baselines import HER, DDPG
#from stable_baselines.her import GoalSelectionStrategy, HERGoalEnvWrapper
#from stable_baselines.ddpg.policies import MlpPolicy

#from stable_baselines import PPO2
#from stable_baselines.common.policies import MlpPolicy

from stable_baselines import DQN
from stable_baselines.deepq.policies import MlpPolicy

import harold_bullet

def main():

    # Create the environment
    env = gym.make("haroldReachBullet-v0")

    print("Observation space:", env.observation_space)
    print("Shape:", env.observation_space.shape)

    try:
        # Load previous model if it exists
        model = DQN.load("HarikdBullet_DeepQ_v1.pkl")
    except:
        # Create the learning agent
        model = DQN(MlpPolicy, env, learning_rate=1e-3, verbose=1)

    env = model.get_env()
    # Train the model using the environment
    model.learn(total_timesteps=100000)

    # Save the trained mode
    model.save("HaroldBullet_DeepQ_v1.pkl")

    obs = env.reset()
    while True:
        for i in range(1000):
            action, _states = model.predict(obs)
            obs, rewards, dones, info = env.step(action)
            env.render()
        
        obs = env.reset()


if __name__ == "__main__":
    main()