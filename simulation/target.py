import pygame


class Target:
    """
    Target class

    + coords: (Tuple[int, int]) coördinaten
    + rect: (pygame.rect) rect
    + sprite: (pygame.surface | None) sprite
    """
    def __init__(
            self, 
            target_data: dict,
            use_gui: bool=False
        ) -> None:
        """
        Initaliser of the Target class
        """

        self.rect = pygame.Rect(target_data["position"], target_data["size"])
        
        self.sprite = None
        if use_gui:
            self.sprite = pygame.image.load(target_data["sprite"])        
            self.sprite = pygame.transform.scale(
                self.sprite, 
                target_data["size"]
            )
