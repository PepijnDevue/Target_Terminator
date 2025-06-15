"""Transition data structure for experience replay."""

from typing import NamedTuple

import numpy as np


class Transition(NamedTuple):
    """
    Data structure representing a single transition in reinforcement learning.
    
    Contains all information needed to store and replay an experience:
    - state: Current state
    - action: Action taken
    - reward: Reward received
    - next_state: Resulting next state
    - terminated: Whether the episode terminated
    """
    state: np.ndarray
    action: int
    reward: float
    next_state: np.ndarray
    terminated: bool
