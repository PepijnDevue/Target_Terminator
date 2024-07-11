import sys
import os
sys.path += ["Target_Terminator/", "Target_Terminator/sssets/"]
try:
    os.chdir('Target_Terminator/')
except:
    pass

from environment.base_env import BaseEnv
from environment.human_rendering_env import HumanRenderingEnv
from environment.human_control_env import HumanControlEnv


def make(render_mode: str=None) -> BaseEnv:
    plane_config = "config/i-16_falangist.yaml"
    env_config = "config/default_env.yaml"
    target_config = "config/default_target.yaml"

    env = None
    match render_mode:
        case "human":
            env = HumanRenderingEnv(plane_config, env_config, target_config)
        case "keyboard":
            env = HumanControlEnv(plane_config, env_config, target_config)
        case _:
            env = BaseEnv(plane_config, env_config, target_config)
    return env
