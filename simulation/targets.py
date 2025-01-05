import numpy as np


class Targets:
    """
    Targets container class.

    This class contains all the targets needed for a simulation. It 
    also contains all the math required to make them act, currently that
    amounts to nothing.

    @public member variables:
    + scalars (np.ndarray): numpy matrix with the following columns:
        0  - mass
        1  - const_drag
        2  - const_lift, alt scalar container 1    
        3  - cl0
        4  - cd_min
        5  - engine_force
        6  - agility
        7  - throttle
        8  - pitch
        9  - coll radius
        10 - AoA_deg 
        11 - entity type flag:
            -1 = nothing, 
            0 = plane, 
            1 = target, 
            2 = bullet
            3 = environment
        12 - collision flag: -1 = alive, 
            otherwise ID of entity that triggered collision
        13 - debug
    + vectors (np.ndarray): numpy matrix with the following columns:
        0 - AoA_crit_low
        1 - AoA_crit_high
        2 - v
        3 - pos 
        4 - v_uv
        5 - f_gravity
        6 - f_engine
        7 - f_drag
        8 - f_lift
        9 - pitch_uv
    
    @public methods:
    + tick())-> None:
        Tick function that currently does nothing.
    """

    def __init__(self, scalars: np.ndarray, vectors: np.ndarray)-> None:
        """
        Initializer for Bullets class.

        Sets self.scalars and self.vectors and sets self.n_bullets to 0.

        @oarams:
            - scalars (np.ndarray): 
            numpy matrix with the following columns:
            0  - mass
            1  - const_drag
            2  - const_lift, alt scalar container 1    
            3  - cl0
            4  - cd_min
            5  - engine_force
            6  - agility
            7  - throttle
            8  - pitch
            9  - coll radius
            10 - AoA_deg 
            11 - entity type flag:
                -1 = nothing, 
                0 = plane, 
                1 = target, 
                2 = bullet
                3 = environment
            12 - collision flag: -1 = alive, 
                otherwise ID of entity that triggered collision
            13 - debug
            - vectors (np.ndarray): 
            numpy matrix with the following columns:
            0 - AoA_crit_low
            1 - AoA_crit_high
            2 - v
            3 - pos 
            4 - v_uv
            5 - f_gravity
            6 - f_engine
            7 - f_drag
            8 - f_lift
            9 - pitch_uv
        """
        self.scalars = scalars
        self.vectors = vectors

    def tick(self)-> None:
        """
        Tick function for targets.
        
        Currently targets have no actions to perform, so the function 
        does nothing.
        """
        pass
