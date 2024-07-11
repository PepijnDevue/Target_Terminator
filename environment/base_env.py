import yaml
import numpy as np
from cerberus import Validator

from simulation.plane import Plane
from simulation.target import Target
from simulation.ground import Ground
from utils.utils import hit_collision_agents
import config.validation_templates as templates


class BaseEnv():
    def __init__(
        self, 
        plane_config: str="config/i-16_falangist.yaml",
        env_config: str="config/default_env.yaml",
        target_config: str="config/default_target.yaml"
    )-> None:
        """
        
        """
        self.dt = 1 / 60
        self.total_time = 0
        
        validator = Validator()
        with open(plane_config, 'r') as stream:
            self.plane_data = yaml.safe_load(stream)
        assert validator.validate(self.plane_data, templates.PLANE_TEMPLATE), \
            f"A validation error occored in the plane data: {validator.errors}"

        with open(env_config, 'r') as stream:
            self.env_data = yaml.safe_load(stream)
        assert validator.validate(self.env_data, templates.ENVIRONMENT_TEMPLATE), \
            f"A validation error occored in the env data: {validator.errors}"

        with open(target_config, 'r') as stream:
            self.target_data = yaml.safe_load(stream)
        assert validator.validate(self.target_data, templates.TARGET_TEMPLATE), \
            f"A validation error occored in the target data: {validator.errors}"


        self.floor = None
        self.agent = None
        self.target = None

        self._create_floor()
        self._create_agent()
        self._create_target()

    def _create_floor(self)-> None:
        self.floor = Ground(self.env_data)

    def _create_agent(self)-> None:
        self.agent = Plane(self.plane_data, self.env_data)

    def _create_target(self)-> None:
        self.target = Target(self.target_data)

    def _calculate_reward(self, state: np.ndarray)-> float:
        """
        State space looks like this:
         - x (float): x position of plane
         - y (float): y position of plane
         - velocity_x (float): velocity of plane in x direction
         - velocity_y (float): velocity of plane in y direction

        NOTE: Function does not check for validty of state parameter.
        """
        return -np.linalg.norm(state[:2] - self.target.rect.center)

    def _check_if_terminated(self)-> bool:
        return hit_collision_agents([self.target], self.agent)
    
    def _check_if_truncated(self)-> bool:
        return self.agent.rot_rect.bottom >= self.floor.coll_elevation

    def _calculate_observation(self)-> np.ndarray:
        state = np.append(self.agent.rot_rect.center, self.agent.v)
        is_terminated = self._check_if_terminated()
        is_truncated = self._check_if_truncated()
        return state, \
            self._calculate_reward(state) + \
                (is_terminated * 1_000_000) + \
                (is_truncated * 1_000_000_000), \
            is_terminated, \
            is_truncated, \
            {}            

    def step(self, action: int)-> np.ndarray:
        match action:
            case 0:
                pass
            case 1:
                self.agent.adjust_pitch(self.dt)
            case 2:
                self.agent.adjust_pitch(-self.dt)
            case 3:
                if self.agent.throttle < 100:
                    self.agent.throttle += self.dt*100
            case 4:
                if self.agent.throttle > 0:
                    self.agent.throttle -= self.dt*100
            case 5:
                pass #bullets
        self.agent.tick(self.dt)

        return self._calculate_observation()

    def reset(self, seed: int=42)-> tuple[np.ndarray, dict]:
        """
        return initial state & info
        """
        self._create_agent()
        self._create_target()

        return np.append(self.agent.rot_rect.center, self.agent.v), {}

        
    def render(self)-> None:
        raise NotImplementedError(
            "As this class has no windows/instances to close, \
            this is not implemented. Perhaps you are looking for del."
        )

    def close(self)-> None:
        pass
