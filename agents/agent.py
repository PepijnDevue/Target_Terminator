"""Agent class for Deep Q-Learning."""

import numpy as np

from environment.base_env import BaseEnv

from .policy import Policy


class Agent:
    """
    Deep Q-Learning Agent.
    
    Implements a basic DQN agent with epsilon-greedy policy.
    Currently uses a placeholder for the Q-network.
    """
    
    def __init__(
        self,
        env: BaseEnv,
        policy: Policy,
    ) -> None:
        """
        Initialize the DQN Agent.
        """
        self.env = env
        self.policy = policy
        
        # Random number generator
        self.rng = np.random.default_rng()

    def act(self, state: np.ndarray) -> np.ndarray:
        """
        Act in the environment based on the current state.
        
        @params:
            - state (np.ndarray): Current state
            
        @returns:
            - np.ndarray: The next state after taking the action
        """
        action = self.policy.select_action(state)
        
        # Execute action in the environment
        next_state, *_ = self.env.step(action)
        
        return next_state
    
    def play(self, steps: int = 10_000) -> None:
        """
        Play the environment for a specified number of steps.
        
        @params:
            - steps (int): Number of steps to play
        """
        state, _ = self.env.reset()
        
        for _ in range(steps):
            state = self.act(state)
            
            # Check if the episode has ended
            if self.env.terminated or self.env.truncated:
                state, _ = self.env.reset()
        
        self.env.close(save_json=True, save_figs=True)