import pygame
import yaml

import utils


class Target:
    """
    Target class

    + coords: (Tuple[int, int]) coördinaten
    + rect: (pygame.rect) rect
    + sprite: (pygame.surface | None) sprite
    """
    def __init__(
            self, 
            target_config: str="config/default_target.yaml",
            use_gui: bool=False
        ) -> None:
        """
        Initaliser of the Target class
        """
        with open(target_config, 'r') as stream:
            target_data = yaml.safe_load(stream)
        assert utils.validate_yaml_data(
            target_data, [
                "sprite", 
                "size", 
                "position"
            ] if not use_gui else [
                "size", 
                "position"
            ]
        ), "Invalid environment config."

        self.rect = pygame.Rect(target_data["position"], target_data["size"])
        
        self.sprite = None
        if use_gui:
            self.sprite = pygame.image.load(target_data["sprite"])        
            self.sprite = pygame.transform.scale(
                self.sprite, 
                target_data["size"]
            )
