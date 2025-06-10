"""Main module for running the Target Terminator environment."""
import random

from __init__ import make

env = make(
    render_mode="keyboard",
    plane_config="config/dickbutt.yaml",
    env_config="config/urinal.yaml",
    target_config="config/fly.yaml",
)

for _ in range(100_000):
    # in keyboard mode the random.choice will be ignored
    state, reward, terminated, truncated, _ = env.step(random.choice([1,2,3,4,5]))
    
    # respawn agent when crashed or won
    if terminated or truncated:
        env.reset()

env.close()
