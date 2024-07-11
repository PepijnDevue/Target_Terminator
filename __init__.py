import sys
import os
sys.path += ["Target_Terminator/", "Target_Terminator/sssets/"]
try:
    os.chdir('Target_Terminator/')
except:
    pass

from environment.env import Env
from environment.human_rendering import Human_rendering
from environment.human_control import Human_control

import settings

def make(render_mode) -> Env:
    window_size: tuple = settings.SCREEN_RESOLUTION 
    match render_mode:
        case "human":
            env = Human_rendering(window_size)
        case "keyboard":
            env = Human_control(window_size)
        case _:
            env = Env(window_size)        
    return env
