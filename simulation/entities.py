"""
Module containing the Entities class.

The Entities class serves as a container for all simulation entities.
It manages airplanes, bullets, targets, and their interactions within the simulation environment.
"""

import numpy as np

from simulation.airplanes import Airplanes
from simulation.bullets import Bullets
from simulation.targets import Targets


class Entities:
    """
    Entities container class.

    This class contains all the entities needed for a simulation. It
    also contains some of the math required to make them act.

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
        12 - collision flag: -1 = alive, 1 if not
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
    + n_planes (int): Number of planes alive.
    + n_targets (int): Number of targets alive.
    + n_bullets (int): Number of bullets alive.
    + n_total (int): Number of objects alive.
    + self.airplanes (Airplanes): All airplanes present in simulation.
    + self.targets (Targets): All targets present in simulation.
    + self.bullets (Bullets): All bullets present in simulation.

    @public methods:
    + tick(self, dt: float, actions: np.ndarray)-> None:
        Tick function to move all objects.
    + spawn_bullet(self, id)-> None:
        Spawn function for new bullets.
    + entity_collision(self)-> None:
        Check for, and resolve, entity collisions.
    """

    def __init__(
        self,
        scalars: np.ndarray,
        vectors: np.ndarray,
        n_entities: int,
        boundaries: np.ndarray,
        plane_data: dict,
    ) -> None:
        """
        Initialize the Entities class.

        Set self.scalars and self.vectors and set all simulation
        objects.

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
            12 - collision flag: -1 = alive, 1 if not
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
            - n_entities (int): Total number of entities present in
            simulation at start.
            - boundaries (np.ndarray): Simulation boundaries with
            shape[[domain_x],[domain_y]], e.g. [[0,1280],[0,720]].
            - plane_data (dict): See plane yamls in config/ for more
            information.
        """
        self.scalars = np.zeros((n_entities, scalars.shape[1]))
        self.vectors = np.zeros((n_entities, vectors.shape[1], 2))
        self.scalars[:,11] = -1
        self.scalars[:,12] = -1

        self.scalars[:scalars.shape[0]] = scalars
        self.vectors[:vectors.shape[0]] = vectors

        # has shape[[domain_x],[domain_y]], e.g. [[0,1280],[0,720]]
        self._boundaries = boundaries

        self.n_planes = np.sum(scalars[:,11]==0)
        self.n_targets = np.sum(scalars[:,11]==1)
        self.n_bullets = 0
        self.n_total = self.n_planes + self.n_targets

        self.airplanes = Airplanes(
            self.scalars[:self.n_planes],
            self.vectors[:self.n_planes],
        )
        self.targets = Targets(
            self.scalars[self.n_planes:self.n_planes+self.n_targets],
            self.vectors[self.n_planes:self.n_planes+self.n_targets],
        )
        self.bullets = Bullets(
            self.scalars[self.n_planes + self.n_targets:],
            self.vectors[self.n_planes + self.n_targets:],
            plane_data,
        )
        # this is the bullet velocity relative to the plane, in m/s
        self._BULLET_SPEED_SCALER = plane_data["bullet_config"]["speed"]
        self._BULLET_COLL_RADIUS = plane_data["bullet_config"]["coll_radius"]

    def tick(self, dt: float, actions: np.ndarray)-> None:
        """
        Tick function to move all objects.
        
        Performs list of actions on all objects, to the extent the delta
        allows for.

        @params:
            - dt (float): Delta time, which controls the severity of the
            performed actions.
            - actions (np.ndarray): List of actions corresponding to the
            number of planes.
        """
        self.airplanes.tick(dt, actions)
        self.bullets.tick(dt)

        self.entity_collision()

        shoot_id = actions[actions[:, 1] == 5]
        if shoot_id.shape[0]!=0:
            self.spawn_bullet(shoot_id[:,0])
        self.n_total += self.bullets.despawn()

    def spawn_bullet(self, id: int)-> None:
        """
        Spawn function for new bullets.

        Create all bullet vectors and pass to self.bullets.

        @params:
            - id (int): id of plane that shot the bullets.
        """
        # the `+ 2` is to make sure there is extra distance between the
        # bounding box of the plane and the radius of the bullet, as to
        # prevent the plane from shooting itself
        pos = self.vectors[id, 3] + self.vectors[id, 4] * \
            (self.scalars[id, 9][:, None] + self._BULLET_COLL_RADIUS + 2)
        v = self.vectors[id, 2] + \
            (self._BULLET_SPEED_SCALER * self.vectors[id, 4])
        vectors = np.zeros((id.shape[0], self.vectors.shape[1], 2))
        vectors[:, 3] = pos
        vectors[:, 2] = v
        self.n_bullets += id.shape[0]
        self.n_total += id.shape[0]
        self.bullets.spawn(vectors)

    def entity_collision(self)-> None:
        """
        Check for, and resolve, entity collisions.

        If any object collides with another, the source ID is saved in
        the destination and the destination object is killed. Since
        the map boundaries are not objects, they will not be killed.
        Instead the source object gets killed.
        """
        mask = (self.scalars[:, 11] != -1) & (self.scalars[:, 12] == -1)
        vectors = self.vectors[mask]
        scalars = self.scalars[mask]

        pos = vectors[:, 3]
        radii = scalars[:, 9]

        d = np.sum((pos[:, np.newaxis] - pos) ** 2, axis=2)
        r = (radii[:, np.newaxis] + radii) ** 2
        np.fill_diagonal(r, -1)
        collision = np.any(d < r, axis=1)

        bounds = (
            pos[:, 0] <= self._boundaries[0, 0]) | (
            pos[:, 0] >= self._boundaries[0, 1]) | (
            pos[:, 1] <= self._boundaries[1, 0]) | (
            pos[:, 1] >= self._boundaries[1, 1]
        )

        # -1 when no collision, 1 when collision
        self.scalars[mask, 12] = np.where(collision | bounds, 1, -1)
