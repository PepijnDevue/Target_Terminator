import datetime  # noqa: D100
import json
import os

import numpy as np
import yaml
from jsonschema import ValidationError, validate

import config.validation_templates as templates
from simulation.entities import Entities
from utils.create_path_plots import create_path_plots
from utils.numpy_encoder import NumpyEncoder

# Define the maximum number of entities that can spawn at the same time.
# Dead bullet entities will not count towards the maximum. Meaning the
# chances of going beyond this limit are very slim.
# !!! CAUTION !!!:
#   Increasing this number may have significant impact on runtime!
MAX_ENTITIES = 1000

class BaseEnv:
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
        Initialize the BaseEnv class.

        @params:
            - plane_config (str): Path to yaml file with plane
            configuration. See config/i-16_falangist.yaml for more info.
            - env_config (str): Path to yaml file with environment
            configuration. See config/default_env.yaml for more info.
            - target_config (str): Path to yaml file with target
            configuration. See config/default_target.yaml for more
            info.
            - seed (int): Seed for randomizer. If None, no seed is used.
        """
        # Initialize random number generators
        self._target_rng = np.random.default_rng(seed)
        self._plane_rng = np.random.default_rng(seed)

        # for saving the observation history, used in self.close()
        self._current_iteration = 0
        self._observation_history = {self._current_iteration : []}

        # delta with which to update the environment each tick
        self._dt = 1 / 60
        
        # validate all of the provided config files
        with open(plane_config, "r") as stream:
            self._plane_data = yaml.safe_load(stream)
        try:
            validate(self._plane_data, templates.PLANE_TEMPLATE)
        except ValidationError as e:
            print(  # noqa: T201
                f"A validation error occurred in the plane data: {e.message}",
            )

        with open(env_config, "r") as stream:
            self._env_data = yaml.safe_load(stream)
        try:
            validate(self._env_data, templates.ENVIRONMENT_TEMPLATE)
        except ValidationError as e:
            print(  # noqa: T201
                f"A validation error occurred in the env data: {e.message}",
            )

        with open(target_config, "r") as stream:
            self._target_data = yaml.safe_load(stream)
        try:
            validate(self._target_data, templates.TARGET_TEMPLATE)
        except ValidationError as e:
            print(  # noqa: T201
                f"A validation error occurred in the target data: {e.message}",
            )

        # reserve memory for necessary member objects
        self._entities = None
        
        self._create_entities()

    def _create_entities(self)-> None:
        """
        Create plane and target entities.

        Uses self._create_agent() and self._create_target() to do this.
        Combines scalars of these two objects into two big matrices,
        which it uses to create an Entities object.
        """
        agent_scalars, agent_vectors = self._create_agent()
        agent_scalars = agent_scalars.reshape((1,) + agent_scalars.shape)
        agent_vectors = agent_vectors.reshape((1,) + agent_vectors.shape)
        target_scalars, target_vectors = self._create_targets()
        
        scalars = np.concatenate((agent_scalars, target_scalars))
        vectors = np.concatenate((agent_vectors, target_vectors))

        window_dimensions = self._env_data["window_dimensions"]
        boundaries = np.array(
            [
                [0,  window_dimensions[0]],
                [0,  window_dimensions[1]],
            ],
        )

        self._entities = Entities(
            scalars=scalars,
            vectors=vectors,
            n_entities=MAX_ENTITIES,
            boundaries=boundaries,
            plane_data=self._plane_data,
        )

    def _create_agent(self)-> tuple[np.ndarray, np.ndarray]:
        """
        Create agent object for self.

        Use plane data to create Plane object.
        
        @returns:
            - tuple with numpy arrays containing scalars and vectors
        """
        scalars = np.array(list(self._plane_data["properties"].values())[:10])
        # randomise spawn pitch based on config
        if self._plane_data["properties"]["max_spawn_pitch_deviation"] > 0:
            pitch_deviation = self._plane_rng.integers(
                low=-self._plane_data["properties"][
                    "max_spawn_pitch_deviation"
                ],
                high=self._plane_data["properties"][
                    "max_spawn_pitch_deviation"
                ],
            )
            scalars[8] += pitch_deviation

        # the extra data is [aoa_degree, entity_type, coll_flag, debug]
        scalars = np.concatenate((scalars, np.array([0, 0, -1, 0])))

        vectors = np.array(
            list(self._plane_data["properties"].values())[10:14],
        )
        # randomise spawn locations based on config
        if self._plane_data["properties"]["max_spawn_position_deviation"] > 0:
            vectors[3] += self._plane_rng.integers(
                low=-self._plane_data["properties"][
                    "max_spawn_position_deviation"
                ],
                high=self._plane_data["properties"][
                    "max_spawn_position_deviation"
                ],
                size=2,
            )
        # update the velocity based on the new pitch
        if self._plane_data["properties"]["max_spawn_pitch_deviation"] > 0:
            pitch_angle_rad = np.radians(pitch_deviation)
            vectors[2] = np.linalg.norm(vectors[2]) * np.array([
                np.cos(pitch_angle_rad),
                np.sin(pitch_angle_rad),
            ])
        # the extra data is
        # v_uv, f_gravity, f_engine, f_drag, f_lift, pitch_uv
        vectors = np.concatenate((vectors, np.zeros(shape=(6,2), dtype=float)))

        return scalars, vectors

    def _create_targets(self)-> tuple[np.ndarray, np.ndarray]:
        """
        Create target object(s) for self.

        Use target data to create Target object.

        @returns:
            - tuple with numpy arrays containing scalars and vectors
        """
        # each key in the target data is equal to a new target,
        # the validation template guarantees this
        n_targets = len(self._target_data)
        scalars = np.zeros(shape=(n_targets, 14))
        vectors = np.zeros(shape=(n_targets, 10, 2))

        for i, target_key in enumerate(list(self._target_data.keys())):
            # set coll radius from template
            scalars[i, 9] = self._target_data[target_key]["coll_radius"]
            # set entity type flag to target
            scalars[i, 11] = 1
            # set collision flag to alive
            scalars[i, 12] = -1

            # set position from template
            vectors[i, 3] = np.array(self._target_data[target_key]["position"])
            
            # randomise spawn location based on config
            if self._target_data[target_key][
                "max_spawn_position_deviation"
            ] > 0:
                vectors[i, 3] += self._target_rng.integers(
                    low=-self._target_data[target_key][
                        "max_spawn_position_deviation"
                    ],
                    high=self._target_data[target_key][
                        "max_spawn_position_deviation"
                    ],
                    size=2,
                )
        return scalars, vectors

    def _calculate_reward(self, state: np.ndarray)-> float:
        """
        Reward function for environment.

        Reward is equal to the difference between the unit vector from
        the plane to the target and the unit vector for the plane's
        velocity will be subtracted. This difference is a value between
        zero and two. It will be multiplied by -100 to make the reward
        fall between -200 and 0. This result will then be multiplied by
        the number of remaining targets, as to punish the agent less the
        more targets it has shot.

        NOTE: function does not check for validity of state parameter

        @params:
            - state (np.ndarray):
            state contains:
                * x (float): x position of plane
                * y (float): y position of plane
                * velocity_x (float): velocity of plane in x direction
                * velocity_y (float): velocity of plane in y direction
                * n_targets (int): number of targets remaining
        
        @returns:
            - float with reward.
        """
        # find closest target for reward
        closest_target_distance = float("inf")
        i_closest_target = None
        for i, (target_scalars, target_vectors) in enumerate(
            zip(self._entities.targets.scalars, self._entities.targets.vectors),
        ):
            if target_scalars[12] == -1:
                distance = np.linalg.norm(target_vectors[3] - state[:2])
                if distance < closest_target_distance:
                    closest_target_distance = distance
                    i_closest_target = i

        if i_closest_target is not None:
            direction_to_target = self._entities.targets.vectors[
                i_closest_target,
                3,
            ] - state[:2]
                
            unit_vector_to_target = direction_to_target / \
                np.linalg.norm(direction_to_target)

            velocity = state[2:4]
            unit_vector_agent = velocity / np.linalg.norm(velocity)

            return -100 * np.linalg.norm(
                unit_vector_agent - unit_vector_to_target,
            ) * state[4]
        # for the last state, if agent succeeded we dont need to
        # calculate any distance, reward should be zero
        return 0
    
    def _check_if_terminated(self)-> bool:
        """
        Check if the current conditions result in a terminal state.

        Terminal state is defined as a state where a bullet collides
        with the target.

        @returns:
            - boolean; True if terminal, False if not
        """
        return np.all(self._entities.targets.scalars[:, 12] != -1)
    
    def _check_if_truncated(self)-> bool:
        """
        Check if the current conditions result in a truncated state.

        Truncated state is defined as a state where the agent crashes.
        For example, the agent can crash into the wall.

        @returns:
            - boolean; True if truncated, False if not
        """
        return np.all(self._entities.airplanes.scalars[:, 12] != -1)

    def _calculate_observation(
            self,
        )-> tuple[np.ndarray, float, bool, bool, dict]:
        """
        Calculate observation of current conditions.

        Observation consists of:
            - state, which contains:
                * x (float): x position of plane
                * y (float): y position of plane
                * velocity_x (float): velocity of plane in x direction
                * velocity_y (float): velocity of plane in y direction
                * n_targets (int): number of targets remaining
            - reward (see self._calculate_reward())
                terminal states are rewarded a bonus,
                whilst truncated states are punished.
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
        pos = self._entities.airplanes.vectors[0, 3]
        v = self._entities.airplanes.vectors[0, 2]
        n_remaining_targets = np.count_nonzero(self._entities.targets.scalars[:, 12] == -1)
        state = np.concatenate(
            (pos, v, np.array(n_remaining_targets)),
            axis=None,
        )
        
        is_terminated = self._check_if_terminated()
        is_truncated = self._check_if_truncated()
        reward = self._calculate_reward(state)
        
        if is_terminated:
            reward += 200
        if is_truncated:
            reward -= 100

        return(state, reward, is_terminated, is_truncated, {})

    def _render(self)-> None:
        """
        Render function for all of the graphical elements of the environment.

        Since the base class does not have any gui elements, this method
        is not implemented here.
        """
        raise NotImplementedError("As this class has no gui, this is not implemented.")

    def step(self, action: int)-> np.ndarray:
        """
        Step function for environment.

        Performs action on agent.
        If the action is shooting, the environment will calculate if the
        bullet will end up hitting the target. If this is the case, the
        reward will be altered with a bonus of 50. If it misses, there
        will be a punishment of -5 reward.

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
        actions = np.array([[0, action]])
        self._entities.tick(self._dt, actions)

        # calculate, save, and return observation in current conditions
        observation = self._calculate_observation()
        self._observation_history[self._current_iteration].append(observation)
        
        # if the action was shoot, alter the reward accordingly
        if action == 5:
            # first bullet is most recent one shot
            bullet_scalars = self._entities.bullets.scalars[0]
            bullet_vectors = self._entities.bullets.vectors[0]
            # calculate remaining bullet lifespan in ticks
            remaining_bullet_lifetime = self._plane_data["bullet_config"] \
                ["lifetime"] - bullet_scalars[2]
            # simulate bullet destination using dt, ticks and velocity
            bullet_destination = bullet_vectors[3] + bullet_vectors[2] * \
                self._dt * remaining_bullet_lifetime

            direction_vector_bullet = bullet_destination - bullet_vectors[3]
            bullet_line_length = np.linalg.norm(direction_vector_bullet)
            norm_direction_vector_bullet = \
                direction_vector_bullet / bullet_line_length

            # get all alive targets
            target_indices = np.where(
                (self._entities.targets.scalars[:, 12] == -1) &
                (self._entities.targets.scalars[:, 13] == 0),
            )[0]
            target_positions = self._entities.targets.vectors[
                target_indices,
                3,
            ]
            target_radii = self._entities.targets.scalars[target_indices, 9]

            # for each target, see if bullet will hit.
            for i, (target_pos, target_rad) in enumerate(
                zip(target_positions, target_radii),
            ):
                # effective radius also takes bullet radius into acount
                effective_radius = bullet_scalars[9] + target_rad

                bullet_start_to_target = target_pos - bullet_vectors[3]
                projection_length = np.dot(
                    bullet_start_to_target,
                    norm_direction_vector_bullet,
                )
                # closest point on the trajectory
                closest_point = bullet_vectors[3] + \
                    norm_direction_vector_bullet * \
                    np.clip(projection_length, 0, bullet_line_length)
                distance_to_center = np.linalg.norm(target_pos- closest_point)

                # if bullet will hit, set debug of target and return
                # positively altered reward
                if distance_to_center <= effective_radius:
                    self._entities.targets.scalars[i, 13] = 1
                    return observation[:1] + \
                        (observation[1] + 50,) + \
                        observation[2:]
            # if bullet does not hit, give small punishment
            return observation[:1] + (observation[1] - 5,) + observation[2:]
        # if no bullets are shot, return observation as is
        return observation

    def reset(self, seed: int|None = None)-> tuple[np.ndarray, dict]:
        """
        Reset environment.

        Will create completely new entities.
        Adds new page to the history dictionary.
        Returns initial state & info.

        @params:
            - seed (int): seed used to spawn in the entities. If None,
            no seed is used.
        
        @returns:
            - np.ndarray with initial state
            (see self._calculate_observation())
            - dict with info, made for compatibility with Gym
            environment, but is always empty.
        """
        if seed is not None:
            self._plane_rng = np.random.default_rng(seed)
            self._target_rng = np.random.default_rng(seed)
        self._create_entities()

        self._current_iteration += 1
        self._observation_history[self._current_iteration] = []

        # the agent's current coordinates are defined by the centre of
        # its rect
        pos = self._entities.airplanes.vectors[0, 3]
        v = self._entities.airplanes.vectors[0, 2]
        n_remaining_targets = len(self._entities.targets.scalars) - \
            np.sum(self._entities.targets.scalars[:, 12])
        return np.concatenate(
            (pos, v, np.array(n_remaining_targets)), axis=None,
        ), {}

    def close(
        self,
        save_json: bool=False,
        save_figs: bool=False,
        figs_stride: int=1,
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
            folder_path = f"output/{datetime.datetime.now().strftime('%d-%m-%Y_%H:%M')}"
            os.mkdir(folder_path)

        # write all the observations to a json file
        if save_json:
            with open(
                f"{folder_path}/_observation_history.json", "w",
            ) as outfile:
                json.dump(self._observation_history, outfile, cls=NumpyEncoder)

        # create all the graphs and save them to the `folder_path`
        if save_figs:
            create_path_plots(
                folder_path,
                self._observation_history,
                self._env_data,
                figs_stride,
            )
