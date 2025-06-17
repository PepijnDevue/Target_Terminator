"""Policy class for epsilon-greedy action selection."""

import numpy as np

from environment.base_env import BaseEnv


class Policy:
    """
    Epsilon-greedy policy for action selection.
    
    Implements epsilon-greedy strategy where the agent either:
    - Exploits: selects the action with highest Q-value
    - Explores: selects a random action
    """
    
    def __init__(
        self,
        epsilon: float = 1.0,
        epsilon_min: float = 0.01,
        epsilon_decay: float = 0.995,
    ) -> None:
        """
        Initialize the epsilon-greedy policy.
        
        @params:
            - epsilon (float): Initial exploration rate
            - epsilon_min (float): Minimum exploration rate
            - epsilon_decay (float): Decay factor for epsilon
            - n_actions (int): Number of possible actions
        """
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay

        self.rng = np.random.default_rng()
        
    def select_action(self, q_values: np.ndarray) -> int:
        """
        Select an action using epsilon-greedy strategy.
        
        @params:
            - state (np.ndarray): Current state (unused in basic implementation)
            
        @returns:
            - int: Selected action
        """
        if self.rng.random() < self.epsilon:
            # Explore: random action
            return self.rng.integers(low=0, high=6)
        
        # Exploit: action with highest Q-value
        return np.argmax(q_values)

    def decay_epsilon(self) -> None:
        """
        Decay the exploration rate epsilon.
        
        Reduces epsilon towards the minimum value to shift from exploration
        to exploitation over time.
        """
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
            self.epsilon = max(self.epsilon, self.epsilon_min)
