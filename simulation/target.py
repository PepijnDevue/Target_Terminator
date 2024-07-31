import pygame
import numpy as np


class Target:
    """
    Target class.

    This is basically the same as the Ground class in ground.py,
    in the sense that it is simply a sprite container that any other
    object can potentially collide with

    @public member variables:
        + rect (pygame.Rect): Rectangle that can be used for collisions.
        + sprite (pygame.Surface | None): Sprite for target.
    """
    def __init__(
            self, 
            target_data: dict,
            use_gui: bool=False
        ) -> None:
        """
        Initializer for the Target class.

        @params:
            - tearget_data (dict): Target configuration. 
            See config/default_target.yaml for more info.
            - use_gui (bool): Toggle to try and load sprite or not.
        """
        position = np.array(np.random.uniform(
            -target_data["position_px_deviation"], 
            target_data["position_px_deviation"],
            2
        )) + np.array(target_data["position"])

        self.rect = pygame.Rect(position, target_data["size"])
        
        self.sprite = None
        if use_gui:
            self.sprite = pygame.transform.scale(
                pygame.image.load(target_data["sprite"]), 
                target_data["size"]
            )
