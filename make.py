from environment import Env
from human_rendering import Human_rendering
from human_control import Human_control

def make(render_mode) -> Env:
    window_size: tuple = (720, 1280) 
    random_target: bool = False
    random_agent: bool = False
    match render_mode:
        case "human":
            env = Human_rendering(window_size, random_agent, random_target)
        case "keyboard":
            env = Human_control(window_size, random_agent, random_target)
        case _:
            env = Env(window_size, random_agent, random_target)
        
    return env

