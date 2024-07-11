import pygame


class Ground:
    """
    Ground class

    + sprite: (pygame.Surface) ground sprite
    + coll_elevation: (int) pixels from top of screen to in-sprite
       ground
    """
    def __init__(
            self, 
            env_data: str="config/default_env.yaml",
            use_gui: bool=False
        )-> None:
        """
        initialiser Ground class
        """

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
