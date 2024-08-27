import pygame
import os
import numpy as np

from environment.base_env import BaseEnv
from simulation.plane import Plane
from simulation.target import Target
from simulation.ground import Ground


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
    + reset(seed: int=42)-> tuple[np.ndarray, dict]
        Resets the environment given a seed. This means that the plane
        and target will be reset to their spawn locations.
    + close()-> None
        Closes the environment and thereby outputs its entire history.
    """

    def __init__(
        self, 
        plane_config: str="config/i-16_falangist.yaml",
        env_config: str="config/default_env.yaml",
        target_config: str="config/default_target.yaml"
    )-> None:
        """
        Initializer for BaseEnv class.

        @params:
            - plane_config (str): Path to yaml file with plane 
            configuration. See config/i-16_falangist.yaml for more info.
            - env_config (str): Path to yaml file with environment 
            configuration. See config/default_env.yaml for more info.
            - target_config (str): Path to yaml file with target 
            configuration. See config/default_target.yaml for more 
            info.
        """
        # place pygame window in top left of monitor(s)
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{0},{0}"
        pygame.init()
            
        super().__init__(
            plane_config=plane_config,
            env_config=env_config,
            target_config=target_config
        )

        # sprite data is not mandatory in config, 
        # so we check these here
        assert "sprite" in self._plane_data and \
            "side_view_dir" in self._plane_data["sprite"] and \
            "top_view_dir" in self._plane_data["sprite"], \
            "Either `sprite`, `sprite : side_view_dir`, or `sprite : "\
            "top_view_dir` are not present in plane data."
        assert "sprite" in self._target_data, "`sprite` key not in target data"
        assert "sprite" in self._env_data["ground"], \
            "`sprite` key not in `ground` field in target data"
        assert "sprite" in self._env_data["background"], \
            "`sprite` key is not in background field in target data"
        
        self.screen = pygame.display.set_mode(
            size=self._env_data["window_dimensions"],
            flags=pygame.DOUBLEBUF
        )
        # self.font = pygame.font.SysFont(None, 24)
        pygame.display.set_caption('Target terminator')

        self._create_background()

    def _create_floor(self)-> None:
        """
        Create floor object for self (with sprite).

        Use environment data to create Ground object.
        """
        self._floor = Ground(self._env_data, True)

    def _create_agent(self)-> None:
        """
        Create agent object for self (with sprite).

        Use plane and environment data to create Plane object.
        """
        self._agent = Plane(self._plane_data, True)

    def _create_target(self)-> None:
        """
        Create target object for self (with sprite).

        Use target data to create Target object.
        """
        self._target = Target(self._target_data, True)


    def _create_background(self)-> None:
        """
        Create background object for self.

        Use environment data to create background object.
        """
        self._background = pygame.image.load(
            self._env_data["background"]["sprite"]
        )
        self._background = pygame.transform.scale(
            self._background,
            self._env_data["window_dimensions"]
        )

    def _render(self)-> None:
        """
        Render function for all of the graphical elements of the 
        environment.
        """
        self.screen.blit(self._background, (0, 0))
        self.screen.blit(self._floor.sprite, [0, self._floor.coll_elevation])
        self.screen.blit(self._target.sprite, self._target.rect)

        for bullet in self._agent.bullets:
            self.screen.blit(bullet.sprite, bullet.rect)

        self.screen.blit(self._agent.sprite, self._agent.rect)
        
        pygame.display.flip()
        
    def step(self, action: int)-> np.ndarray:
        """
        Step function for environment.

        Performs action on self._agent and renders frame.

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
        step_info = super().step(action=action)

        self._render()

        return step_info
    
    def reset(self, seed: int=42)-> tuple[np.ndarray, dict]:
        """
        Reset environment.

        Will create completely new agent and target.
        Adds new page to the history dictionary
        return initial state & info. Renders the initial frame

        @params:
            - seed (int): seed used to spawn in the agent and target.
        
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
        figs_stride: int=1
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
        """
        pygame.display.quit()
        pygame.quit()
        super().close(
            save_json=save_json, 
            save_figs=save_figs,
            figs_stride=figs_stride
        )
