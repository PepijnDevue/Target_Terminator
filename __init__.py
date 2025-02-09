"""
Initializer file for TargetTerminator/ folder.

This file enables constructions like:
```py
import Target_Terminator as TT

TT.make()
```
"""

import sys
import os

# set the system path correctly, so the assets and configurations will
# be correctly selected
# add '' to the system path so the directory of the script that's being
# run is also included
# https://stackoverflow.com/questions/49559003/why-is-the-first-element-in-pythons-sys-path-an-empty-string
sys.path += ["", "Target_Terminator/", "Target_Terminator/assets/"]

# if possible, set the directory of the os
try:
    os.chdir('Target_Terminator/')
except:
    pass

from environment.base_env import BaseEnv
from environment.human_rendering_env import HumanRenderingEnv
from environment.human_control_env import HumanControlEnv


def make(
    render_mode: str=None, 
    plane_config: str="config/i-16_falangist.yaml",
    env_config: str="config/default_env.yaml",
    target_config: str="config/default_target.yaml",
    seed: int=None
) -> BaseEnv:
    """
    Make function for Target_Terminator

    Makes one of:
        - Environment without gui.
        - Environment with gui.
        - Environment with gui, where the agent can be controlled by
        the user, using their keyboard.
    
    @params:
        - render_mode (str): Render mode, to make gui, keyboard gui, or
        neither.
        - plane_config (str): Path to yaml file with plane 
        configuration. See config/i-16_falangist.yaml for more info.
        - env_config (str): Path to yaml file with environment 
        configuration. See config/default_env.yaml for more info.
        - target_config (str): Path to yaml file with target 
        configuration. See config/default_target.yaml for more 
        info.
        - seed (int): Seed for randomizer. If None, no seed is used.
    """
    env = None
    match render_mode:
        case "human":
            env = HumanRenderingEnv(
                plane_config, 
                env_config, 
                target_config, 
                seed
            )
        case "keyboard":
            env = HumanControlEnv(
                plane_config, 
                env_config, 
                target_config, 
                seed
            )
        # anything that is not "human" or "keyboard" gets interpreted
        # as no gui.
        case _:
            env = BaseEnv(plane_config, env_config, target_config, seed)
    return env
