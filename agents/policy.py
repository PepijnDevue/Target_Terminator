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
        env: BaseEnv,
        alpha: float = 0.01,
        gamma: float = 0.99,
        epsilon: float = 1.0,
        epsilon_min: float = 0.01,
        epsilon_decay: float = 0.995,
        n_actions: int = 6,
    ) -> None:
        """
        Initialize the epsilon-greedy policy.
        
        @params:
            - epsilon (float): Initial exploration rate
            - epsilon_min (float): Minimum exploration rate
            - epsilon_decay (float): Decay factor for epsilon
            - n_actions (int): Number of possible actions
        """
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.n_actions = n_actions

        self.rng = np.random.default_rng()

        self._train(env)
        
    def select_action(self, state: np.ndarray) -> int:
        """
        Select an action using epsilon-greedy strategy.
        
        @params:
            - state (np.ndarray): Current state (unused in basic implementation)
            
        @returns:
            - int: Selected action
        """
        if self.rng.random() < self.epsilon:
            # Explore: random action
            return self.rng.integers(0, self.n_actions)
        
        # Placeholder for exploitation logic
        return self.rng.integers(0, self.n_actions)
    
    def _train(self, env: BaseEnv) -> None:
        pass
    
    def _decay(self) -> None:
        """Decay epsilon to reduce exploration over time."""
        if self.epsilon >= self.epsilon_min:
            self.epsilon = max(
                self.epsilon_min,
                self.epsilon * self.epsilon_decay,
            )
