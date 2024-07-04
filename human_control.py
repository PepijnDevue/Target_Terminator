from human_rendering import Human_rendering

import pygame


class Human_control(Human_rendering):
    def __init__(
        self, 
        window_size: tuple, 
        random_target: bool=False, 
        random_agent: bool=False
    )-> None:
        super().__init__(
            window_size=window_size,
            random_target=random_target, 
            random_agent=random_agent
        )

    def step(self, action=0):
        action = 0 # action parameter not used for this mode
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            action = 1
        elif keys[pygame.K_DOWN]:
            action = 2
        elif keys[pygame.K_RIGHT]:
            action = 3
        elif keys[pygame.K_LEFT]:
            action = 4
        elif keys[pygame.K_SPACE]:
            action = 5

        return super().step(action=action)

