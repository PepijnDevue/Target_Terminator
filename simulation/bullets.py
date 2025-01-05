import numpy as np


class Bullets:
    """
    Bullets container class.

    This class contains all the bullets needed for a simulation. It 
    also contains all the math required to make them move.

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
    + n_bullets (int): Number of bullets alive at present time.
    
    @public methods:
    + tick(dt: float)-> None:
        Tick function to move all bullets.
    + spawn(self, vectors: np.ndarray)-> None:
        Spawn function for new bullets.
    + despawn(self)-> int:
        Despawn function for bullets.
    """

    def __init__(
            self, 
            scalars: np.ndarray, 
            vectors: np.ndarray, 
            plane_data: dict
        )-> None:
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
        self.n_bullets = 0
        self._BULLET_LIFESPAN = plane_data["bullet_config"]["lifetime"]
        self._BULLET_COLL_RADIUS = plane_data["bullet_config"]["coll_radius"]
        self.scalars[:, 9] += self._BULLET_COLL_RADIUS
        
    def tick(self, dt: float)-> None:
        """
        Tick function to update cl0 of all bullets.

        @params:
            - dt (float): Delta time, which controls the severity of the
            performed actions.
        """
        self.vectors[:self.n_bullets, 3] += \
            dt * self.vectors[:self.n_bullets, 2]

    def spawn(self, vectors: np.ndarray)-> None:
        """
        Spawn function for new bullets.

        Adds all bullet vectors in the front of the matrix and sets 
        flags where needed.

        @params:
            - vectors (np.ndarray): Vectors with data of new bullets.
        """
        n = vectors.shape[0]
        self.n_bullets += n
        self.scalars[n:] = self.scalars[:-n]
        self.vectors[n:] = self.vectors[:-n]
        self.scalars[:n, 2] = 0
        self.scalars[:n, 9] = self._BULLET_COLL_RADIUS
        self.scalars[:n, 11] = 2
        self.scalars[:n, 12] = -1
        self.vectors[:n] = vectors

    def despawn(self)-> int:
        """
        Despawn function for bullets.
        
        Checks and marks all bullets that are dead and subtracts them 
        from total.

        @returns:
            int with number of destroyed bullets.
        """
        # index 2 of scalars is being used as lifespan timer for bullets
        self.scalars[:self.n_bullets, 2] += 1
        n = np.count_nonzero(
            self.scalars[:self.n_bullets, 2] > self._BULLET_LIFESPAN
        )
        self.scalars[self.n_bullets - n : self.n_bullets, 11] = -1
        self.n_bullets -= n
        return n
