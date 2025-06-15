"""Main module for running the Target Terminator environment."""
import random

from __init__ import Agent, Policy, make

PLANE_CONFIG = "config/dickbutt.yaml"
ENV_CONFIG = "config/urinal.yaml"
TARGET_CONFIG = "config/fly.yaml"

def run_headed(mode: str = "keyboard") -> None:
    """
    Run the environment in headed mode with GUI or keyboard control.

    This function initializes the environment with the specified render mode
    and runs a simulation for a specified number of steps. The agent can be
    controlled via keyboard input or runs autonomously in GUI mode.

    @param mode: Render mode for the environment. Options are "human", "keyboard
    ", or "headless". Defaults to "keyboard".
    """
    env = make(
        render_mode=mode,
        plane_config=PLANE_CONFIG,
        env_config=ENV_CONFIG,
        target_config=TARGET_CONFIG,
    )

    for _ in range(10_000):
        # in keyboard mode the random.choice will be ignored
        state, reward, terminated, truncated, _ = env.step(random.choice([1,2,3,4,5]))
        
        # respawn agent when crashed or won
        if terminated or truncated:
            env.reset()

    env.close(
        save_json=True,
        save_figs=True,
    )


def run_headless() -> None:
    """
    Run the environment in headless mode.
    
    This function initializes the environment without any GUI and runs
    a simulation for a specified number of steps.
    """
    env = make(
        render_mode="headless",
        plane_config=PLANE_CONFIG,
        env_config=ENV_CONFIG,
        target_config=TARGET_CONFIG,
    )

    policy = Policy(env)  # Placeholder for policy initialization

    agent = Agent(env, Policy)  # Placeholder for agent initialization

    agent.play() # Placeholder for agent's play method


if __name__ == "__main__":
    mode = input("Enter render mode: ").strip().lower()

    match mode:
        case "k" | "keyboard":
            run_headed("keyboard")
        case "h" | "human":
            run_headed("human")
        case _:
            run_headless()