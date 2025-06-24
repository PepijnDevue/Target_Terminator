"""Policy class for epsilon-greedy action selection."""

import numpy as np
import torch

from .dqn import DeepQNetwork
from .transition import Transition


class Policy:
    """
    Epsilon-greedy policy for action selection.
    
    Implements epsilon-greedy strategy where the agent either:
    - Exploits: selects the action with highest Q-value
    - Explores: selects a random action
    """
    
    def __init__(
        self,
        dqn: DeepQNetwork,
        epsilon: float = 1.0,
        epsilon_min: float = 0.01,
        epsilon_decay: float = 0.995,
        discount_factor: float = 0.99,
    ) -> None:
        """
        Initialize the epsilon-greedy policy.
        
        @params:
            - dqn (DeepQNetwork): The deep Q-network for action value estimation
            - epsilon (float): Initial exploration rate
            - epsilon_min (float): Minimum exploration rate
            - epsilon_decay (float): Decay factor for epsilon
            - learning_rate (float): Learning rate for Q-value updates
            - discount_factor (float): Discount factor for future rewards
        """
        self.dqn = dqn
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.gamma = discount_factor

        self.rng = np.random.default_rng()
        
    def select_action(self, state: np.ndarray) -> int:
        """
        Select an action using epsilon-greedy strategy.
        
        @params:
            - state (np.ndarray): Current state (unused in basic implementation)
            
        @returns:
            - int: Selected action
        """
        q_values = self.dqn(torch.tensor(state, dtype=torch.float32))

        # Decay epsilon after each action selection
        self.decay_epsilon()

        if self.rng.random() < self.epsilon:
            # Explore: random action
            return self.rng.integers(low=0, high=6)
        
        # Exploit: action with highest Q-value
        return np.argmax(q_values)
    
    def train(self, batch: list[Transition]) -> None:
        """
        Train the DQN using a batch of transitions.
        
        Updates the Q-values based on the Bellman equation.
        
        @params:
            - batch (list[Transition]): Batch of transitions for training
        """
        states = torch.stack([torch.tensor(t.state, dtype=torch.float32) for t in batch])
        actions = torch.tensor([t.action for t in batch], dtype=torch.long)
        rewards = torch.tensor([t.reward for t in batch], dtype=torch.float32)
        next_states = torch.stack([torch.tensor(t.next_state, dtype=torch.float32) for t in batch])
        terminated = torch.tensor([bool(t.terminated) for t in batch], dtype=torch.bool)

        q_values = self.dqn(states)

        next_q_values = self.dqn(next_states).max(dim=1)[0]
        next_q_values[terminated] = 0.0

        # Compute target Q-values using the Bellman equation
        target_q_values = q_values.clone()
        target_q_values[torch.arange(len(batch)), actions] = (
            rewards + self.gamma * next_q_values
        )

        # Finally, call update with the computed target Q-values shape (batch_size, num_actions)
        self.dqn.update(states, target_q_values)

    def decay_epsilon(self) -> None:
        """
        Decay the exploration rate epsilon.
        
        Reduces epsilon towards the minimum value to shift from exploration
        to exploitation over time.
        """
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
            self.epsilon = max(self.epsilon, self.epsilon_min)
