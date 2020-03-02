import os
import sys

try:
    timesteps = sys.argv[1]
except IndexError:
    timesteps=30000

models = os.listdir("models")

model_version = 0

if len(models) > 0:
    if len(models) <= 9:
        model_version = models[-1][-1:]
    elif len(models) > 9:
        model_version = models[-1][-2:]

curr_model = f"Harold_HER_v{str(model_version)}"
new_version = int(model_version) + 1
new_model = f"Harold_HER_v{str(new_version)}"

if model_version == 0:
    cmd = f"python -m baselines.run --alg=her --env=HaroldReach-v0 --num_timesteps={timesteps} --save_path=./models/{new_model} --log_path=./logs/{new_model}logs"
else:
    cmd = f"python -m baselines.run --alg=her --env=HaroldReach-v0 --num_timesteps={timesteps} --load_path=./models/{curr_model} --save_path=./models/{new_model} --log_path=./logs/{new_model}_logs"

os.system(cmd)
