from environment import Env

def make(**kwargs) -> Env:
    human_rendering = False
    if kwargs.get("render_mode") == "human":
        human_rendering = True
        



make(render_mode="human")

