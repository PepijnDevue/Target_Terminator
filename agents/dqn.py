"""DeepQNetwork Class for Deep Q-Learning Function Approximation."""

import numpy as np
import torch
from torch import nn


class DeepQNetwork(nn.Module):
    """
    Deep Q-Network (DQN) for Q-value function approximation.
    
    A Multi-Layer Perceptron (MLP) that predicts Q-values for each action
    given the current state. The network architecture follows the specification:
    - Input layer: 5 features (state dimensions)
    - Hidden layer 1: 150 neurons with ReLU activation
    - Hidden layer 2: 128 neurons with ReLU activation
    - Output layer: 6 neurons (one for each action)
    
    Uses Mean Squared Error (MSE) loss for training.
    """
    
    def __init__(
        self,
        learning_rate: float = 0.001,
        input_size: int = 5,
        hidden_size1: int = 150,
        hidden_size2: int = 128,
        output_size: int = 6
    ) -> None:
        """
        Initialize the DQN network.
        """
        super().__init__()
        
        self.layers = nn.Sequential(
            nn.Linear(input_size, hidden_size1),
            nn.ReLU(),
            nn.Linear(hidden_size1, hidden_size2),
            nn.ReLU(),
            nn.Linear(hidden_size2, output_size),
        )

        self.optimizer = torch.optim.Adam(self.parameters(), lr=learning_rate)

    def forward(self, x: np.ndarray) -> torch.Tensor:
        """
        Forward pass through the network.
        
        @params:
            - x (np.ndarray): Input state
        @returns:
            - torch.Tensor: Predicted Q-values for each action
        """
        x_tensor = torch.tensor(x, dtype=torch.float32)
        return self.layers(x_tensor)
    
    def __call__(self, x: np.ndarray) -> torch.Tensor:
        """
        Make the network callable directly.
        
        @params:
            - x (np.ndarray): Input state
        @returns:
            - torch.Tensor: Predicted Q-values for each action
        """
        return self.forward(x)
