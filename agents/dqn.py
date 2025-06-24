"""DeepQNetwork Class for Deep Q-Learning Function Approximation."""

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
        load: bool = True,
        learning_rate: float = 0.001,
        input_size: int = 5,
        hidden_size1: int = 150,
        hidden_size2: int = 128,
        output_size: int = 6,
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
        
        if load:
            try:
                self.layers.load_state_dict(torch.load("agents/models/dqn.pth"))
            except FileNotFoundError:
                print("No pre-trained model found. Initializing a new model.") # noqa: T201

        self.optimizer = torch.optim.Adam(self.parameters(), lr=learning_rate)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass through the network.
        
        @params:
            - x (torch.Tensor): Input state(s) - can be single state or batch of states
        @returns:
            - torch.Tensor: Predicted Q-values for each action
        """
        # Ensure input has batch dimension
        if x.dim() == 1:
            x = x.unsqueeze(0)

        return self.layers(x)
    
    def __call__(self, x: torch.Tensor) -> torch.Tensor:
        """
        Make the network callable directly. Detached from PyTorch's autograd.
        
        @params:
            - x (torch.Tensor): Input state
        @returns:
            - torch.Tensor: Predicted Q-values for each action
        """
        return self.forward(x).detach()
    
    def update(self, states: torch.Tensor, target_q_values: torch.Tensor) -> None:
        """
        Update the network parameters using backpropagation.
        
        @params:
            - states (torch.Tensor): Input states
            - target_q_values (torch.Tensor): Target Q-values for training
        """
        # Zero gradients from previous step
        self.optimizer.zero_grad()
        
        # Forward pass
        predicted_q_values = self.forward(states)

        # Compute loss
        loss = nn.MSELoss()(predicted_q_values, target_q_values)

        # Backward pass
        loss.backward()

        # Update parameters
        self.optimizer.step()

    def save(self, filename: str = "dqn") -> None:
        """
        Save the model parameters to a file.
        
        @params:
            - filename (str): Path to the file where the model will be saved
        """
        # Add paths "agents/models + filename
        torch.save(self.layers.state_dict(), f"agents/models/{filename}.pth")
