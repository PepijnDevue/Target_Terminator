import pygame
import math


class Bullet:
    """
    Bullet class

    This class instantiates a bullet that conforms to physics given the
    environment.

    @public member variables:
        + rect (pygame.Rect): Rectangle that can be used for collisions.
        + sprite: (pygame.Surface) Sprite for bullet
    """
    def __init__(
            self,
            bullet_data: dict,
            position: tuple[int, int],
            pitch: float,
            use_gui: bool=False
    )-> None:
        """
        Initaliser of the Bullet class

        @params:
            - bullet_data (dict): Bullet configuration. 
            See config/i-16_falangist.yaml for more info.
            - position (tuple[int, int]): Starting position of the bullet.
            - pitch (float): Pitch of the bullet.
            - use_gui (bool): Toggle to try and load sprite or not.
        """
        self.starting_pos = position
        self.rect = pygame.Rect(self.starting_pos, bullet_data["size"])
        
        self.speed_x = bullet_data["speed"] * \
            math.cos(math.radians(-pitch))
        self.speed_y = bullet_data["speed"] * \
            math.sin(math.radians(-pitch))
        self.lifetime = bullet_data["lifetime"]

        self.sprite = None
        if use_gui:
            self.sprite = pygame.transform.scale(
                pygame.image.load(bullet_data["sprite"]),
                bullet_data["size"]
            )
            self.sprite = pygame.transform.rotate(
                self.sprite,
                pitch
            )

    def update(self)-> None:
        """
        Update the position of the bullet.
        """
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
