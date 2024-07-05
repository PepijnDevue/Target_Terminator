from agent import Agent
from target import Target
from utils import hit_collision_agents
import numpy as np
import settings
import ground

class Env():
    def __init__(
        self, 
        window_size: tuple
    )-> None:
        
        self.window_size = window_size

        self.dt = 1 / 60
        self.total_time = 0

        self.agent = None

        self.target = None

        self._create_object_instances()

    def _create_object_instances(self):
        self.floor = ground.Ground(
            height=settings.GROUND["HEIGHT"],
            elevation=settings.GROUND["ELEVATION"],
            coll_elevation=settings.GROUND["COLL_ELEVATION"],
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

    def _calculate_reward(self, state: np.ndarray)-> float:
        """
        State space looks like this:
         - x (float): x position of plane
         - y (float): y position of plane
         - velocity_x (float): velocity of plane in x direction
         - velocity_y (float): velocity of plane in y direction

        NOTE: Function does not check for validty of state parameter
        """
        return -np.linalg.norm(state[:2] - self.target.rect.center)

    def _check_if_terminated(self)-> bool:
        return hit_collision_agents([self.target], self.agent)
    
    def _check_if_truncated(self)-> bool:
        return self.agent.rot_rect.bottom >= self.floor.coll_elevation

    def _calculate_observation(self)-> np.ndarray:
        state = np.append(self.agent.pos_real, self.agent.v)
        is_terminated = self._check_if_terminated()
        is_truncated = self._check_if_truncated()
        return state, \
            self._calculate_reward(state) + \
                (is_terminated * 1_000_000) + \
                (is_truncated * 1_000_000_000), \
            is_terminated, \
            is_truncated            

    def step(self, action: int):
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
        self.agent.tick(self.dt, None)

        return self._calculate_observation()

    def reset(self):
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
        raise NotImplementedError(
            "As this class has no windows/instances to close, \
            this is not implemented. Perhaps you are looking for del."
        )

    def close(self):
        self.__del__()