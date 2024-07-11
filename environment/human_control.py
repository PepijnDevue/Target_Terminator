import pygame

from environment.human_rendering import Human_rendering


class Human_control(Human_rendering):
    def __init__(
        self, 
        plane_config: str="config/i-16_falangist.yaml",
        env_config: str="config/default_env.yaml"
    )-> None:
        super().__init__(
            plane_config=plane_config,
            env_config=env_config
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

