import pygame
import numpy as np

from simulation.deprecated.plane import Plane
from simulation.deprecated.target import Target


def check_target_agent_collision(target: Target, agent: Plane) -> bool:
    """
    This function checks if the player hits a target. If a player
    hits a target, the function returns True.

    @params:
        - target (target): Target to check for.
        - agent (Plane): Agent to check for.
    
    @returns:
        - bool, True if agent rect collides with target, False if not.
    """
    return pygame.Rect.colliderect(target.rect, agent.rect)

def check_bullet_collision(
        agent: Plane, 
        target: Target,
        floorheight: int,
        window_width: int
    )-> bool:
    """
    This function checks all the entity_collision a bullet could experience. If
    a bullet hits a target, the function returns True

    @params:
        - target (target): Target to check for.
        - agent (Plane): Agent that fired the bullets.
        - floorheight (int): height of the floor.
        - window_width (int): width of the window

    @returns:
        - bool, True if a bullet rect collides with target, 
        False if not.
    """
    target_hit = False
    remaining_bullets = []

    for bullet in agent.bullets:
        if (np.linalg.norm((
                bullet.rect.centerx - bullet.starting_pos[0], 
                bullet.rect.centery - bullet.starting_pos[1]
            )) > bullet._lifetime or
            bullet.rect.bottom >= floorheight or
            bullet.rect.top < -10 or
            bullet.rect.left < -10 or 
            bullet.rect.right > window_width + 10
        ):  
            continue
        elif pygame.Rect.colliderect(bullet.rect, target.rect):
            target_hit = True
        else:
            remaining_bullets.append(bullet)

    agent.bullets = remaining_bullets

    return target_hit
