import sys
import os
sys.path += ["Target_Terminater/", "Target_Terminater/sssets/"]
try:
    os.chdir('Target_Terminater/')
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
