from environment import Env

import settings
import ground
import pygame


class Human_rendering(Env):
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

        self.dt = 0

        self.clock = pygame.time.Clock()

        self.screen = None

        self.floor = ground.Ground(
            height=settings.GROUND["HEIGHT"], 
            elevation=settings.GROUND["ELEVATION"],
            coll_elevation=settings.GROUND["COLL_ELEVATION"],
            sprite=settings.GROUND["SPRITE"],
            resolution=settings.SCREEN_RESOLUTION
        )

        self.background = pygame.image.load("assets/background.png")
        self.background = pygame.transform.scale(
            self.background,
            settings.SCREEN_RESOLUTION
        )

    def render(self):
        if self.screen is None:
            pygame.init()
            self.screen = pygame.display.set_mode(
                size=settings.SCREEN_RESOLUTION,
                flags=pygame.DOUBLEBUF
            )
            self.font = pygame.font.SysFont(None, 24)
            pygame.display.set_caption('Target terminator')
        
        self.screen.fill("white")
        self.screen.blit(self.background, (0, 0))

        self.screen.blit(self.floor.sprite, [0, self.floor.elevation])
        self.screen.blit(self.agent.rot_sprite, self.agent.rot_rect)
        self.screen.blit(self.target.sprite, self.target.coords)
        
        self.dt = self.clock.tick(settings.FPS) / 1000
        self.total_time += self.dt

        pygame.display.flip()
        
    def step(self, action: int):
        super().step(action=action)

        self.render()

    def close(self):
        pygame.display.quit()
        pygame.quit()