from agent import Agent
from target import Target
from settings import PLANE_I_16_REPUBLICAN as plane
from settings import TARGET as target

import numpy as np
import settings
import ground

class Env():
    def __init__(
        self, 
        window_size: tuple,
        random_target: bool=False, 
        random_agent: bool=False
    )-> None:
        
        self.window_size = window_size

        
        self.dt = 1 / 60
        self.total_time = 0

        self.floor = ground.Ground(
            height=settings.GROUND["HEIGHT"],
            elevation=settings.GROUND["ELEVATION"],
            coll_elevation=settings.GROUND["COLL_ELEVATION"],
        )

        if not random_agent:
            self.agent = Agent(
                settings.SCREEN_RESOLUTION,
                plane["SPRITE"],
                plane["SPRITE_TOP"],
                plane["MASS"],
                plane["ENGINE_FORCE"],
                plane["AGILITY"],
                plane["C_DRAG"],
                plane["C_LIFT"],
                plane["AOA_CRIT_LOW"],
                plane["AOA_CRIT_HIGH"],
                plane["CL0"],
                plane["CD_MIN"],
                plane["INIT_THROTTLE"],
                0.0, # Start pitch
                plane["INIT_V"],
                np.array((50, self.window_size[0] / 2)) / settings.PLANE_POS_SCALE % settings.SCREEN_RESOLUTION,
                plane["SIZE"]
            )
        
        if not random_target:
            self.target = Target(self.floor.coll_elevation, target["SPRITE"])
            self.target.coords = (self.window_size[1] - 50, self.window_size[0] / 2)

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

        return None

    def reset(self):
        pass

    def render(self):
        pass

    def close(self):
        pass