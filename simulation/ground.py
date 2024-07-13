import pygame


class Ground:
    """
    Ground class.

    This class is primarily a container for an image that is collidable
    with the plane. It is configured to be a floor object

    @public member variables:
        + sprite (None | pygame.Surface): sprite for ground, if provided
        + coll_elevation (int): y value (from top) for the collision
    """
    def __init__(
            self, 
            env_data: dict,
            use_gui: bool=False
        )-> None:
        """
        Initializer for Ground class.

        @params:
            - env_data (dict): environment configuration.
            See config/default_env.yaml for more info.
            - use_gui (bool) toggle to try and load sprite or not
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
