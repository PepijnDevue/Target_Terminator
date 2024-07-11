import pygame
import os
import numpy as np

from environment.base_env import BaseEnv
from simulation.plane import Plane
from simulation.target import Target
from simulation.ground import Ground
import settings


class HumanRenderingEnv(BaseEnv):
    def __init__(
        self, 
        plane_config: str="config/i-16_falangist.yaml",
        env_config: str="config/default_env.yaml",
        target_config: str="config/default_target.yaml"
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
            plane_config=plane_config,
            env_config=env_config,
            target_config=target_config
        )

        self._create_background()

        # sprite data is not manditory in config, 
        # so we check these here
        assert "sprite" in self.plane_data and \
            "side_view_dir" in self.plane_data["sprite"] and \
            "top_view_dir" in self.plane_data["sprite"], \
            "Either `sprite`, `sprite : side_view_dir`, or `sprite : "\
            "top_view_dir` are not present in plane data."
        assert "sprite" in self.target_data, "`sprite` key not in target data"
        assert "sprite" in self.env_data["ground"], \
            "`sprite` key not in `ground` field in target data"
        

    def _create_floor(self)-> None:
        self.floor = Ground(self.env_data, True)

    def _create_agent(self)-> None:
        self.agent = Plane(self.plane_data, self.env_data, True)

    def _create_target(self)-> None:
        self.target = Target(self.target_data, True)


    def _create_background(self)-> None:
        self.background = pygame.image.load("assets/background.png")
        self.background = pygame.transform.scale(
            self.background,
            settings.SCREEN_RESOLUTION
        )

    def render(self)-> None:
        self.screen.blit(self.background, (0, 0))

        self.screen.blit(self.floor.sprite, [0, self.floor.coll_elevation])
        self.screen.blit(self.agent.rot_sprite, self.agent.rot_rect)
        self.screen.blit(self.target.sprite, self.target.rect)
        
        self.total_time += self.dt

        pygame.display.flip()
        
    def step(self, action: int)-> np.ndarray:
        step_info = super().step(action=action)

        self.render()

        return step_info
    
    def reset(self, seed: int=42)-> tuple[np.ndarray, dict]:
        super().reset()

        self.render()


    def close(self)-> None:
        pygame.display.quit()
        pygame.quit()
    