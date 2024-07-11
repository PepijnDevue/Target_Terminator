import pygame
import numpy as np

from environment.human_rendering_env import HumanRenderingEnv


class HumanControlEnv(HumanRenderingEnv):
    def __init__(
        self, 
        plane_config: str="config/i-16_falangist.yaml",
        env_config: str="config/default_env.yaml",
        target_config: str="config/default_target.yaml"
    )-> None:
        super().__init__(
            plane_config=plane_config,
            env_config=env_config,
            target_config=target_config
        )

    def step(self, action=0)-> np.ndarray:
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
