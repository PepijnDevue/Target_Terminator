import yaml
import datetime
import json
import os
import numpy as np
from cerberus import Validator

from simulation.plane import Plane
from simulation.target import Target
from simulation.ground import Ground
from utils.collision import check_target_agent_collision
from utils.numpy_encoder import NumpyEncoder
from utils.create_path_plots import create_path_plots
import config.validation_templates as templates


class BaseEnv():
    """
    Base environment class.

    This class instantiates an entire environment, excluding a GUI.
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
        # for saving the observation history, used in self.close()
        self._current_iteration = 0
        self._observation_history = {self._current_iteration : []}

        # delta with which to update the environment each tick
        self._dt = 1 / 60

        # validate all of the provided config files
        validator = Validator()
        with open(plane_config, 'r') as stream:
            self._plane_data = yaml.safe_load(stream)
        assert validator.validate(
            self._plane_data, 
            templates.PLANE_TEMPLATE
        ), f"A validation error occurred in the plane data: {validator.errors}"

        with open(env_config, 'r') as stream:
            self._env_data = yaml.safe_load(stream)
        assert validator.validate(
            self._env_data, 
            templates.ENVIRONMENT_TEMPLATE
        ), f"A validation error occurred in the env data: {validator.errors}"

        with open(target_config, 'r') as stream:
            self._target_data = yaml.safe_load(stream)
        assert validator.validate(
            self._target_data, 
            templates.TARGET_TEMPLATE
        ),f"A validation error occurred in the target data: {validator.errors}"

        # calculate max distance, to normalize reward
        self._max_distance = np.linalg.norm(
            self._env_data["window_dimensions"]
        )

        # reserve memory for necessary member objects
        self._floor = None
        self._agent = None
        self._target = None

        # initialize member objects
        self._create_floor()
        self._create_agent()
        self._create_target()

    def _create_floor(self)-> None:
        """
        Create floor object for self.

        Use environment data to create Ground object.
        """
        self._floor = Ground(self._env_data)

    def _create_agent(self)-> None:
        """
        Create agent object for self.

        Use plane and environment data to create Plane object.
        """
        self._agent = Plane(self._plane_data, self._env_data)

    def _create_target(self)-> None:
        """
        Create target object for self.

        Use target data to create Target object.
        """
        self._target = Target(self._target_data)

    def _calculate_reward(self, state: np.ndarray)-> float:
        """
        Reward function for environment.

        Reward is equal to the negative of the absolute distance from
        the agent to the target, divided by the maximum distance the 
        plane could travel, to normalize it. Additionally, the 
        difference between the unit vector from the plane to the target
        and the unit vector for the plane's velocity will be subtracted.

        NOTE: function does not check for validity of state parameter

        @params:
            - state (np.ndarray): 
            state contains:
                * x (float): x position of plane
                * y (float): y position of plane
                * velocity_x (float): velocity of plane in x direction
                * velocity_y (float): velocity of plane in y direction
        
        @returns:
            - float with reward.
        """
        direction_to_target = self._target.rect.center - state[:2]

        unit_vector_to_target = direction_to_target / \
            np.linalg.norm(direction_to_target)

        velocity = state[2:4]
        unit_vector_agent = velocity / np.linalg.norm(velocity)

        return (
            -100 * np.linalg.norm(direction_to_target) / self._max_distance
        ) -50 * np.linalg.norm(unit_vector_agent - unit_vector_to_target) 

    def _check_if_terminated(self)-> bool:
        """
        Check if the current conditions result in a terminal state.

        Terminal state is defined as a state where the agent collides
        with the target.

        @returns:
            - boolean; True if terminal, False if not
        """
        return check_target_agent_collision(self._target, self._agent)
    
    def _check_if_truncated(self)-> bool:
        """
        Check if the current conditions result in a truncated state.

        Truncated state is defined as a state where the agent crashes.
        For example, the agent can crash into the ground.

        @returns:
            - boolean; True if truncated, False if not
        """
        agent_rect = self._agent.rect
        window_width = self._env_data["window_dimensions"][0]
        return (
            agent_rect.bottom >= self._floor.coll_elevation or
            agent_rect.top < -10 or
            agent_rect.left < -10 or
            agent_rect.right > window_width + 10
        )

    def _calculate_observation(
            self
        )-> tuple[np.ndarray, float, bool, bool, dict]:
        """
        Calculate observation of current conditions.

        Observation consists of:
            - state, which contains:
                * x (float): x position of plane
                * y (float): y position of plane
                * velocity_x (float): velocity of plane in x direction
                * velocity_y (float): velocity of plane in y direction
            - reward (see self._calculate_reward())
                terminal states are rewarded a bonus of 1,000,000, 
                whilst truncated states are rewarded with -1,000,000,000
            - is_terminal (see self._check_if_terminal)
            - is_truncated (see self._check_if_truncated)
            - info, made for compatibility with Gym environment, 
            but is always empty.

        @returns:
             - np.ndarray with state
             - float with reward
             - bool with is_terminal
             - bool with is_truncated
             - dict with info (always empty)
        """
        state = np.append(self._agent.rect.center, self._agent.v)
        is_terminated = self._check_if_terminated()
        is_truncated = self._check_if_truncated()
        reward = self._calculate_reward(state)
        
        if is_terminated:
            reward += 200
        if is_truncated:
            reward -= 1_000

        return(state, reward, is_terminated, is_truncated, {})

    def _render(self)-> None:
        """
        Render function for all of the graphical elements of the 
        environment.

        Since the base class does not have any gui elements, this method
        is not implemented here.
        """
        raise NotImplementedError(
            "As this class has no gui, this is not implemented."
        )

    def step(self, action: int)-> np.ndarray:
        """
        Step function for environment.

        Performs action on self._agent.

        @params:
            - action (int): one of:
                * 0: do nothing
                * 1: adjust pitch upwards
                * 2: adjust pitch downwards
                * 3: increase throttle
                * 4: decrease throttle
                * 5: shoot a bullet
        
        @returns:
            - np.ndarray with observation of resulting conditions
        """
        # do nothing
        if action == 0:
            pass
        # adjust pitch upwards
        elif action == 1:
            self._agent.adjust_pitch(self._dt)
        # adjust pitch downwards
        elif action == 2:
            self._agent.adjust_pitch(-self._dt)
        # increase throttle, to a max of 100
        elif action == 3:
            if self._agent.throttle < 100:
                self._agent.throttle += self._dt * 100
        # decrease throttle, to a min of 0
        elif action == 4:
            if self._agent.throttle > 0:
                self._agent.throttle -= self._dt * 100
        # shoot a bullet
        elif action == 5:
            raise NotImplementedError("shooting is not yet possible")
        # any other actions are invalid
        else:
            raise ValueError(
                f"Provided with action {action}, "
                "which is not one of [0,1,2,3,4,5]"
            )
        
        # update the agent with adjusted settings
        self._agent.tick(self._dt)

        # calculate, save, and return observation in current conditions
        observation = self._calculate_observation()
        self._observation_history[self._current_iteration].append(observation)

        return observation

    def reset(self, seed: int=42)-> tuple[np.ndarray, dict]:
        """
        Reset environment.

        Will create completely new agent and target.
        Adds new page to the history dictionary.
        Returns initial state & info.

        @params:
            - seed (int): seed used to spawn in the agent and target.
        
        @returns:
            - np.ndarray with initial state 
            (see self._calculate_observation())
            - dict with info, made for compatibility with Gym 
            environment, but is always empty.
        """
        self._create_agent()
        self._create_target()

        self._current_iteration += 1
        self._observation_history[self._current_iteration] = []

        # the agent's current coordinates are defined by the centre of 
        # its rect
        return np.append(self._agent.rect.center, self._agent.v), {}

    def close(
        self, 
        save_json: bool=False, 
        save_figs: bool=False, 
        figs_stride: int=1
    )-> None:
        """
        Close environment and output history.

        Will create a folder indicated by the current date and time, 
        provided save == True in which resides:
            - a json file with the entire observation history.
            - an image per iteration, which displays the flown path of 
            the agent, along with the reward (indicated by the colour).
        
        @params:
            - save_json (bool): Save json or not.
            - save_figs (bool): Save the plots or not.
            - figs_stride (int): Stride for saving the figures.
        """
        # prepare the output folder
        if save_json or save_figs:
            folder_path = "output/" \
            f"{datetime.datetime.now().strftime('%d-%m-%Y_%H:%M')}"
            os.mkdir(folder_path)

        # write all the observations to a json file
        if save_json:
            with open(
                f"{folder_path}/_observation_history.json", "w"
            ) as outfile: 
                json.dump(self._observation_history, outfile, cls=NumpyEncoder)

        # create all the graphs and save them to the `folder_path`
        if save_figs:
            create_path_plots(
                folder_path, 
                self._observation_history, 
                self._env_data,
                figs_stride
            )
