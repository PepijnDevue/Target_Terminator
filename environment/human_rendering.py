from environment.env import Env
from simulation.agent import Agent
from simulation.target import Target

import numpy as np
import settings
from simulation.ground import Ground
import pygame
import os


class Human_rendering(Env):
    def __init__(
        self, 
        window_size: tuple
    )-> None:
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{0},{0}"
        pygame.init()
            
        self.screen = pygame.display.set_mode(
            size=settings.SCREEN_RESOLUTION,
            flags=pygame.DOUBLEBUF
        )
        self.font = pygame.font.SysFont(None, 24)
        pygame.display.set_caption('Target terminator')

        super().__init__(
            window_size=window_size
        )

    def _create_object_instances(self):
        self.floor = Ground(
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
        
        self.agent = Agent(
            settings.SCREEN_RESOLUTION,
            settings.PLANE_I_16_FALANGIST["SPRITE"],
            settings.PLANE_I_16_FALANGIST["SPRITE_TOP"],
            settings.PLANE_I_16_FALANGIST["MASS"],
            settings.PLANE_I_16_FALANGIST["ENGINE_FORCE"],
            settings.PLANE_I_16_FALANGIST["AGILITY"],
            settings.PLANE_I_16_FALANGIST["C_DRAG"],
            settings.PLANE_I_16_FALANGIST["C_LIFT"],
            settings.PLANE_I_16_FALANGIST["AOA_CRIT_LOW"],
            settings.PLANE_I_16_FALANGIST["AOA_CRIT_HIGH"],
            settings.PLANE_I_16_FALANGIST["CL0"],
            settings.PLANE_I_16_FALANGIST["CD_MIN"],
            settings.PLANE_I_16_FALANGIST["INIT_THROTTLE"],
            0.0, # Start pitch
            settings.PLANE_I_16_FALANGIST["INIT_V"],
            np.array((50, self.window_size[1] / 2)) / settings.PLANE_POS_SCALE % settings.SCREEN_RESOLUTION,
            settings.PLANE_I_16_FALANGIST["SIZE"]
        )

        self.target = Target(self.floor.coll_elevation, settings.TARGET["SPRITE"], (self.window_size[0] - 50, self.window_size[1] / 2))

    def render(self):
        self.screen.blit(self.background, (0, 0))

        self.screen.blit(self.floor.sprite, [0, self.floor.elevation])
        self.screen.blit(self.agent.rot_sprite, self.agent.rot_rect)
        self.screen.blit(self.target.sprite, self.target.rect)
        
        self.total_time += self.dt

        pygame.display.flip()
        
    def step(self, action: int):
        step_info = super().step(action=action)

        self.render()

        return step_info
    
    def reset(self, seed: int=42):
        super().reset()

        self.render()


    def close(self):
        pygame.display.quit()
        pygame.quit()