"""Main module for running the Target Terminator environment."""
import random

from __init__ import Agent, DeepQNetwork, Policy, make

PLANE_CONFIG = "config/dickbutt.yaml"
ENV_CONFIG = "config/urinal.yaml"
TARGET_CONFIG = "config/fly.yaml"

def run_keyboard() -> None:
    """
    Run the environment in headed mode with GUI or keyboard control.

    This function initializes the environment with the specified render mode
    and runs a simulation for a specified number of steps. The agent can be
    controlled via keyboard input or runs autonomously in GUI mode.

    @param mode: Render mode for the environment. Options are "human", "keyboard
    ", or "headless". Defaults to "keyboard".
    """
    env = make(
        render_mode="keyboard",
        plane_config=PLANE_CONFIG,
        env_config=ENV_CONFIG,
        target_config=TARGET_CONFIG,
    )

    for _ in range(10_000):
        # in keyboard mode the random.choice will be ignored
        _, _, terminated, truncated, _ = env.step(0)
        
        # respawn agent when crashed or won
        if terminated or truncated:
            env.reset()

    env.close(
        save_json=False,
        save_figs=False,
    )


def run_ai(mode: str = "headless") -> None:
    """
    Run the environment in headless mode.
    
    This function initializes the environment without any GUI and runs
    a simulation for a specified number of steps.
    """
    env = make(
        render_mode=mode,
        plane_config=PLANE_CONFIG,
        env_config=ENV_CONFIG,
        target_config=TARGET_CONFIG,
    )

    dqn = DeepQNetwork(load=True)

    policy = Policy(dqn)

    agent = Agent(env, policy, training=False)

    agent.play(10_000)


if __name__ == "__main__":
    mode = input("Enter render mode: ").strip().lower()

    match mode:
        case "k" | "keyboard":
            run_keyboard()
        case "h" | "human":
            run_ai("human")
        case _:
            run_ai()
