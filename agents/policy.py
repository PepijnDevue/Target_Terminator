"""Policy class for epsilon-greedy action selection."""

import numpy as np


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
        learning_rate: float = 1, # Zit al in DQN, dus hier 1?
        discount_factor: float = 0.99,
    ) -> None:
        """
        Initialize the epsilon-greedy policy.
        
        @params:
            - epsilon (float): Initial exploration rate
            - epsilon_min (float): Minimum exploration rate
            - epsilon_decay (float): Decay factor for epsilon
            - learning_rate (float): Learning rate for Q-value updates
            - discount_factor (float): Discount factor for future rewards
        """
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.alpha = learning_rate
        self.gamma = discount_factor

        self.rng = np.random.default_rng()
        
    def select_action(self, q_values: np.ndarray) -> int:
        """
        Select an action using epsilon-greedy strategy.
        
        @params:
            - state (np.ndarray): Current state (unused in basic implementation)
            
        @returns:
            - int: Selected action
        """
        # Decay epsilon after each action selection
        self.decay_epsilon()

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
    
    def compute_target_q_values(
        self,
        q_values: np.ndarray,
        action: int,
        reward: float,
        next_q_value: float,
    ) -> np.ndarray:
        """
        Compute target Q-values using the Bellman equation.
        
        @params:
            - q_values (np.ndarray): Current Q-values
            - action (int): Action taken
            - reward (float): Reward received
            - next_q_value (float): Maximum Q-value for the next state
            
        @returns:
            - np.ndarray: Updated Q-values
        """
        target_q_values = q_values.copy()
        
        q_value = q_values[action]
                
        target_q_values[action] += self.alpha * (reward + self.gamma * next_q_value - q_value)
        
        return target_q_values
