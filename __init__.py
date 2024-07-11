import sys
import os
sys.path += ["Target_Terminator/", "Target_Terminator/sssets/"]
try:
    os.chdir('Target_Terminator/')
except:
    pass

from environment.base_env import BaseEnv
from environment.human_rendering import Human_rendering
from environment.human_control import Human_control

import settings

def make(render_mode: str=None) -> BaseEnv:
    plane_config = "config/i-16_falangist.yaml"
    env_config = "config/default_env.yaml"
    match render_mode:
        case "human":
            env = Human_rendering(plane_config, env_config)
        case "keyboard":
            env = Human_control(plane_config, env_config)
        case _:
            env = BaseEnv(plane_config, env_config)        
    return env
