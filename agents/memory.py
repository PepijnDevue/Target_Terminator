"""Memory class for experience replay buffer."""

import random
from collections import deque

from .transition import Transition


class Memory:
    """
    Experience replay buffer using deque for storing transitions.
    
    Stores transitions and provides random sampling for training.
    """
    
    def __init__(self, capacity: int = 10_000) -> None:
        """
        Initialize the memory buffer.
        
        @params:
            - capacity (int): Maximum number of transitions to store
        """
        self.capacity = capacity
        self.buffer = deque(maxlen=capacity)
        self.rng = random.Random()
    
    def store(self, transition: Transition) -> None:
        """
        Store a transition in the memory buffer.
        
        @params:
            - transition (Transition): The transition to store
        """
        self.buffer.append(transition)
    
    def sample(self, batch_size: int) -> list[Transition]:
        """
        Sample a batch of transitions from the memory buffer.
        
        @params:
            - batch_size (int): Number of transitions to sample
            
        @returns:
            - List[Transition]: List of sampled transitions
            
        @raises:
            - ValueError: If batch_size is larger than available transitions
        """
        if batch_size > len(self.buffer):
            msg = f"Cannot sample {batch_size} transitions from buffer of size {len(self.buffer)}"
            raise ValueError(msg)
        
        return self.rng.sample(list(self.buffer), batch_size)
    
    def __len__(self) -> int:
        """Return the current number of transitions stored."""
        return len(self.buffer)
    
    def is_ready(self, batch_size: int) -> bool:
        """
        Check if the buffer has enough transitions for sampling.
        
        @params:
            - batch_size (int): Required batch size
            
        @returns:
            - bool: True if buffer has enough transitions
        """
        return len(self.buffer) >= batch_size
