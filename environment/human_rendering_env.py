"""
Human Rendering Environment module for Target Terminator.

This module provides a pygame-based graphical interface for the simulation environment,
allowing for real-time visualization of the plane, targets, and bullets.
"""

import os

import numpy as np
import pygame

from environment.base_env import BaseEnv


class HumanRenderingEnv(BaseEnv):
    """
    Base environment class.

    This class instantiates an entire environment, including a GUI.
    It creates the environment, plane, and target, as stated in the
    provided config files.

    This class has no public member variables.

    @public methods:
    + step(action: int)-> np.ndarray
        Takes a step in the environment. This means that the plane
        will be updated based on the action taken and that the
        environment will react accordingly.
    + reset(seed: int=None)-> tuple[np.ndarray, dict]
        Resets the environment given a seed. This means that the plane
        and target will be reset to their spawn locations.
    + close(
        save_json: bool=False,
        save_figs: bool=False,
        figs_stride: int=1
      )-> None
        Closes the environment and thereby outputs its entire history.
    """

    def __init__(
        self,
        plane_config: str="config/i-16_falangist.yaml",
        env_config: str="config/default_env.yaml",
        target_config: str="config/default_target.yaml",
        seed: int|None = None,
    )-> None:
        """
        Initialize HumanRenderingEnv class.

        @params:
            - plane_config (str): Path to yaml file with plane
            configuration. See config/i-16_falangist.yaml for more info.
            - env_config (str): Path to yaml file with environment
            configuration. See config/default_env.yaml for more info.
            - target_config (str): Path to yaml file with target
            configuration. See config/default_target.yaml for more
            info.
            - seed (int): seed for randomizer. If None, no seed is used.
        """
        # place pygame window in top left of monitor(s)
        os.environ["SDL_VIDEO_WINDOW_POS"] = f"{0},{30}"
        pygame.init()
        
        # Initialize the clock for FPS control
        self.clock = pygame.time.Clock()
            
        super().__init__(
            plane_config=plane_config,
            env_config=env_config,
            target_config=target_config,
            seed=seed,
        )

        # sprite data is not mandatory in config,
        # so we check these here
        if "sprite" not in self._plane_data:
            raise ValueError("`sprite` key not in plane data.")
        if "side_view_dir" not in self._plane_data["sprite"]:
            raise ValueError("`side_view_dir` key not in plane data['sprite'].")
        
        for target_key in self._target_data:
            if "sprite" not in self._target_data[target_key]:
                raise ValueError(f"`sprite` key not in target data['{target_key}']")
        
        if "sprite" not in self._env_data["background"]:
            raise ValueError("`sprite` key is not in background field in target data")
        
        self.screen = pygame.display.set_mode(
            self._env_data["window_dimensions"],
        )
        
        pygame.display.set_caption("Target terminator")

        self._create_sprites()

    def _create_sprites(self)-> None:
        """
        Create background object for self.

        Use environment data to create background object.
        """
        self._background_sprite = pygame.image.load(
            self._env_data["background"]["sprite"],
        )
        self._background_sprite = pygame.transform.scale(
            self._background_sprite,
            pygame.display.get_surface().get_size(),
        )

        self._target_sprites = [pygame.transform.scale(
            pygame.image.load(self._target_data[target_key]["sprite"]),
            self._target_data[target_key]["size"],
        ) for target_key in self._target_data]

        self._bullet_sprite = pygame.transform.scale(
            pygame.image.load(self._plane_data["bullet_config"]["sprite"]),
            self._plane_data["bullet_config"]["size"],
        )

        self._plane_sprite = pygame.transform.scale(
            pygame.image.load(self._plane_data["sprite"]["side_view_dir"]),
            self._plane_data["sprite"]["size"],
        )

    def _render(self) -> None:
        """
        Render function for all of the graphical elements of the environment.

        This function draws the background, targets, bullets, and planes to the screen.
        """
        # gather all rotation instructions for bullets and save to tuple
        alive_bullets = self._entities.bullets.vectors[(
            (self._entities.bullets.scalars[:, 12] == -1) &
            (self._entities.bullets.scalars[:, 11] != -1)
        )]

        rotate_instructions = (
            np.degrees(
                np.arctan2(alive_bullets[:, 2, 0], alive_bullets[:, 2, 1]),
            ) + 270
        ) % 360

        blit_data_bullets = []
        for bullet_vectors, rotate_instruction in zip(
            alive_bullets,
            rotate_instructions,
            strict=True,
        ):
            rotated_sprite = pygame.transform.rotate(
                self._bullet_sprite,
                rotate_instruction,
            )
            # use coordinates as center for sprite
            bullet_rect = rotated_sprite.get_rect()
            bullet_rect.center = bullet_vectors[3]
            blit_data_bullets.append((rotated_sprite, bullet_rect.topleft))

        # gather all rotation instructions for planes and save to tuple
        alive_airplanes = self._entities.airplanes.vectors[
            (self._entities.airplanes.scalars[:, 12] == -1)
        ]

        rotate_instructions = self._entities.airplanes.scalars[
            (self._entities.airplanes.scalars[:, 12] == -1)
        ][:, 8]

        blit_data_planes = []
        for airplane_vectors, rotate_instruction in zip(
            alive_airplanes,
            rotate_instructions,
            strict=True,
        ):
            rotated_sprite = pygame.transform.rotate(
                self._plane_sprite,
                rotate_instruction,
            )
            # use coordinates as center for sprite
            plane_rect = rotated_sprite.get_rect()
            plane_rect.center = airplane_vectors[3]
            blit_data_planes.append((rotated_sprite, plane_rect.topleft))

        # put target sprite(s) position in center
        blit_data_targets = []
        for i, target_sprite in enumerate(self._target_sprites):
            if self._entities.targets.scalars[i, 12] == -1:
                target_rect = target_sprite.get_rect()
                target_rect.center = self._entities.targets.vectors[i, 3]
                blit_data_targets.append((target_sprite, target_rect.topleft))

        # blit all objects in order of background, target, bullet, plane
        self.screen.blits(
            blit_sequence=[
                # Background
                (self._background_sprite, (0, 0)),
                *blit_data_targets,
                *blit_data_bullets,
                *blit_data_planes,
            ],
        )
        
        pygame.display.flip()
        
        # Limit the tick rate to the specified TPS from config
        tps = self._env_data.get("tps", 1000)
        self.clock.tick(tps)

        
    def step(self, action: int)-> np.ndarray:
        """
        Step function for environment.

        Performs action on agent and renders frame.

        @params:
            - action (int): one of:
                * 0:  do nothing
                * 1: adjust pitch upwards
                * 2: adjust pitch downwards
                * 3: increase throttle
                * 4: decrease throttle
                * 5: shoot a bullet
        
        @returns:
            - np.ndarray with observation of resulting conditions
        """
        # check if the game has bene quit, which case the game is closed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # if you close the environment mid run, we assume you
                # do not want to save the run information
                self.close()

        step_info = super().step(action=action)

        self._render()

        return step_info
    
    def reset(self, seed: int | None=None)-> tuple[np.ndarray, dict]:
        """
        Reset environment.

        Will create completely new entities.
        Adds new page to the history dictionary
        return initial state & info. Renders the initial frame

        @params:
            - seed (int): seed used to spawn in the entities. If None,
            no seed is used.
        
        @returns:
            - np.ndarray with initial state
            (see self._calculate_observation()).
            - dict with info, made for compatibility with Gym
            environment, but is always empty.
        """
        output = super().reset(seed=seed)

        self._render()

        return output

    def close(
        self,
        save_json: bool=False,
        save_figs: bool=False,
        figs_stride: int=1,
    )-> None:
        """
        Close environment and output history.

        Will create a folder indicated by the current date and time
        in which resides:
            - a json file with the entire observation history.
            - an image per iteration, which displays the flown path of
            the agent, along with the reward (indicated by the colour).

        @params:
            - save_json (bool): Save json or not.
            - save_figs (bool): Save the plots or not.
            - figs_stride (int): Stride for saving the figures.
        """
        pygame.display.quit()
        pygame.quit()
        super().close(
            save_json=save_json,
            save_figs=save_figs,
            figs_stride=figs_stride,
        )
