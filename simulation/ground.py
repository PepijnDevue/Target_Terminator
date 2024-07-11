import pygame
import yaml

import utils


class Ground:
    """
    Ground class

    + sprite: (pygame.Surface) ground sprite
    + coll_elevation: (int) pixels from top of screen to in-sprite
       ground
    """
    def __init__(
            self, 
            env_config: str="config/default_env.yaml",
            use_gui: bool=False
        )-> None:
        """
        initialiser Ground class
        """
        with open(env_config, 'r') as stream:
            env_data = yaml.safe_load(stream)
        assert utils.validate_yaml_data(
            env_data, 
            ((
                "window_dimensions", []
            ), (
                "ground", [
                    "sprite",
                    "height",
                    'collision_elevation'
                ] if use_gui else [
                    "height",
                    'collision_elevation'
                ]
            ))
        ), "Invalid environment config."

        self.sprite = None
        if use_gui:
            self.sprite = pygame.transform.scale(
                pygame.image.load(env_data["ground"]["sprite"]), 
                (
                    env_data["window_dimensions"][0], 
                    env_data["ground"]["height"]
                )
            )

        self.coll_elevation = env_data["ground"]["collision_elevation"]
