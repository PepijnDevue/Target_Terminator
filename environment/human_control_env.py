"""
Human Control Environment Module.

This module provides the HumanControlEnv class that allows a human user
to control the plane in the simulation using keyboard inputs.
"""

import numpy as np
import pygame

from environment.human_rendering_env import HumanRenderingEnv


class HumanControlEnv(HumanRenderingEnv):
    """
    Human control environment class.

    This class instantiates an entire environment, including a GUI.
    It creates the environment, plane, and target, as stated in the
    provided config files. It allows the user to fly the plane using
    their keyboard. This can be useful in debugging, and also quite fun.

    This class has no public member variables.

    @public methods:
    + step(action: int)-> np.ndarray
        Takes a step in the environment. This means that the plane
        will be updated based on the action taken and that the
        environment will react accordingly.
    + reset(seed: int=None)-> tuple[np.ndarray, dict]
        Resets the environment given a seed. This means that the plane
        and target will be reset to their spawn locations.
    + close(
        save_json: bool=False,
        save_figs: bool=False,
        figs_stride: int=1
      )-> None
        Closes the environment and thereby outputs its entire history.
    """

    def step(self, action: int=0)-> np.ndarray:
        """
        Step function for human control environment.

        This function checks for user input and passes it to the super.

        @params:
            - action (int): action to take.
            NOTE: Parameter is always ignored.
        
        @returns:
            - np.ndarray with observation of resulting conditions
        """
        # provided action argument is ignored as this instance should
        # be controlled manually
        action = 0

        keys = pygame.key.get_pressed()
        # up = pitch up
        if keys[pygame.K_UP]:
            action = 1
        # down = pitch down
        elif keys[pygame.K_DOWN]:
            action = 2
        # right = increase throttle
        elif keys[pygame.K_RIGHT]:
            action = 3
        # left = decrease throttle
        elif keys[pygame.K_LEFT]:
            action = 4
        # space = shoot a bullet
        elif keys[pygame.K_SPACE]:
            action = 5

        return super().step(action=action)
