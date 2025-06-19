"""Agent class for Deep Q-Learning."""

import numpy as np

from environment.base_env import BaseEnv

from .dqn import DeepQNetwork
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
        dqn: DeepQNetwork,
        memory_capacity: int = 10_000,
        training: bool = True,
    ) -> None:
        """
        Initialize the DQN Agent.
        
        @params:
            - env (BaseEnv): The environment to interact with
            - policy (Policy): The policy for action selection
            - dqn (DeepQNetwork): The deep Q-network
            - memory_capacity (int): Maximum number of transitions to store in memory
        """
        self.env = env
        self.policy = policy
        self.dqn = dqn
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
        q_values = self.dqn(self.state)

        action = self.policy.select_action(q_values)
        
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

        for transition in batch:
            q_values = self.dqn(transition.state)
            
            # Calculate the next Q-value (0 if terminated)
            next_q_value = 0
            if not transition.terminated:
                next_q_value = self.dqn(transition.next_state).max()
            
            # Use policy to compute target Q-values using Bellman equation
            target_q_values = self.policy.compute_target_q_values(
                q_values=q_values,
                action=transition.action,
                reward=transition.reward,
                next_q_value=next_q_value,
            )
            
            # Update the DQN network
            self.dqn.update(transition.state, target_q_values)

    def play(self, steps: int = 10_000) -> None:
        """
        Play the environment for a specified number of steps.
        
        @params:
            - steps (int): Number of steps to play
        """
        # TODO: save dqn
        try:
            self.state, _ = self.env.reset()
            
            for _ in range(steps):
                self.act()
            
            self.env.close(save_json=True, save_figs=True)
        except KeyboardInterrupt:
            print("Training interrupted by user.") # noqa: T201
            self.env.close(save_json=True, save_figs=True)
