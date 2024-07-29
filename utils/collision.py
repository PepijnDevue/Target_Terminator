import pygame

from simulation.plane import Plane
from simulation.target import Target


def check_target_agent_collision(
        target: Target,
        agent: Plane
    ) -> bool:
    """
    This function checks if the player hits a target. If a player
    hits a target, the function returns True.

    @params:
        - target (target): Target to check for.
        - agent (Plane): Agent to check for.
    
    @returns:
        - bool, True if collision agent is within 10 pixels of the 
        target, False if not.
    """
    return pygame.Rect.colliderect(target.rect, agent.rect)
