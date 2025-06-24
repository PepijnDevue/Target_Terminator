"""Agent class for Deep Q-Learning."""

import numpy as np
import pygame

from environment.base_env import BaseEnv

from .memory import Memory
from .policy import Policy
from .transition import Transition


class Agent:
    """
    Deep Q-Learning Agent.
    
    Implements a basic DQN agent with epsilon-greedy policy and experience replay.
    Stores transitions in memory buffer for potential training.
    """
    
    def __init__(
        self,
        env: BaseEnv,
        policy: Policy,
        memory_capacity: int = 10_000,
        training: bool = True,
    ) -> None:
        """
        Initialize the DQN Agent.
        
        @params:
            - env (BaseEnv): The environment to interact with
            - policy (Policy): The policy for action selection
            - memory_capacity (int): Maximum number of transitions to store in memory
        """
        self.env = env
        self.policy = policy
        self.memory = Memory(capacity=memory_capacity)
        self.rng = np.random.default_rng()
        self.state = None
        self.training = training

    def act(self) -> np.ndarray:
        """
        Act in the environment based on the current state.
        
        Stores the transition in memory for potential future learning.
            
        @returns:
            - np.ndarray: The next state after taking the action
        """
        action = self.policy.select_action(self.state)
        
        # Execute action in the environment
        next_state, reward, terminated, truncated, _ = self.env.step(action)

        # Store transition in memory
        transition = Transition(
            state=self.state,
            action=action,
            reward=reward,
            next_state=next_state,
            terminated=terminated or truncated, # Beide?
        )
        self.memory.store(transition)

        if self.training:
            self.train()

        if terminated or truncated:
            # Reset the environment if the episode has ended
            next_state, _ = self.env.reset()
        
        self.state = next_state

    def train(self) -> None:
        """
        Train the DQN agent using the stored transitions in memory.
        
        This method samples a batch of transitions from memory and updates
        the DQN network based on the Q-learning algorithm.
        """
        if len(self.memory) < self.memory.batch_size:
            return
        
        batch = self.memory.sample()

        self.policy.train(batch)

    def play(self, steps: int = 40_000) -> None:
        """
        Play the environment for a specified number of steps.
        
        @params:
            - steps (int): Number of steps to play
        """
        try:
            self.state, _ = self.env.reset()
            
            for _ in range(steps):
                self.act()
            
            self.env.close(save_json=True, save_figs=True)
            self.policy.dqn.save()
        except (KeyboardInterrupt, pygame.error):
            print("Training interrupted by user.") # noqa: T201
            self.env.close(save_json=True, save_figs=True)
            self.policy.dqn.save()
