import pygame
import math
import numpy as np

from typing import List
from simulation.bullet import Bullet


class Plane:
    """
    Plane class.

    This class instantiates a plane that conforms to physics, given the
    environment.

    @public member variables:
        + sprite: (pygame.Surface) side view sprite
        + rect: (pygame.Rect) rectangle object for pygame
        + throttle: (float) throttle
        + v: (tuple[float, float]) velocity vector
    
    @private member variables:
    NOTE: normally not explained, as they are private, but here they are
    kept due to their complexity.
        - _mass: (float) mass of aircraft, in kilogram (Kg).
        - _engine_force: (float) constant force applied in direction
        of `pitch` in Newtons (N)
        - _agility: (float) Degree to which the pitch can change,
        in degrees per delta.
        - _c_drag: (float) 'constants' when calculating drag,
        such as air density and wing area
        - _c_lift: (float) 'constants' when calculating lift,
        such as air density and wing area
        - _AoA_crit_low: (tuple[float, float]) negative critical angle
        of attack in degrees and its corresponding lift coefficient
        - _AoA_crit_high: (tuple[float, float]) positive critical angle
        of attack in degrees and its corresponding lift coefficient
        - _cl0: (float) lift coefficient at AoA == 0
        - _cd_min: (float) apex of drag curve; 
        drag coefficient at AoA == 0
        - _plane_size: (tuple[int, int]) dimensions of aircraft
        (length, height) in meter (m)
        - _pitch: (float) pitch in degrees
        - _AoA_deg: (float) angle of attack in deg
        - _pitch_uv: (tuple[float, float]) unitvector corresponding to
        `pitch`
        - _v_uv: (tuple[float, float]) unitvector corresponding to `v`
        - _f_gravity: (tuple[float, float]) gravity force vector
        - _f_engine: (tuple[float, float]) engine force vector
        - _f_drag: (tuple[float, float]) drag force vector
        - _f_lift: (tuple[float, float]) drag force vector

    @public methods:
    + def tick(dt: float)-> None:
        Update all the member variables of plane, provided their current
        states and the provided delta.
    + def adjust_pitch(dt: float)-> None:
        Adjust the pitch of the agent, provided the given delta.
    """
    def __init__(
        self,
        plane_data: dict,
        use_gui: bool=False
    )-> None:
        """
        Initializer for Plane class.

        @params:
            - plane_data (dict): Plane configuration. 
            See config/i-16_falangist.yaml for more info.
            - use_gui (bool): Toggle to try and load sprite or not.
        """
        # Constants
        self._mass = plane_data["properties"]["mass"]
        self._engine_force = plane_data["properties"]["engine_force"]
        self._agility = plane_data["properties"]["agility"]
        self._const_drag = plane_data["properties"]["drag_constant"]
        self._const_lift = plane_data["properties"]["lift_constant"]
        self._AoA_crit_low = plane_data["properties"][
            "critical_aoa_lower_bound"
        ]
        self._AoA_crit_high = plane_data["properties"][
            "critical_aoa_higher_bound"
        ]
        self._cl0 = plane_data["properties"]["lift_coefficient_aoa_0"]
        self._cd_min = plane_data["properties"]["drag_coefficient_aoa_0"]

        # Independent Variables
        self.throttle = plane_data["starting_config"]["initial_throttle"]
        self._pitch = plane_data["starting_config"]["initial_pitch"]
        self.v = np.array(plane_data["starting_config"]["initial_velocity"])

        # Dependent variables (oa Numpy containers)
        self._AoA_deg = 0
        self.pitch_uv = np.array([0.0, 0.0])
        self._v_uv = np.array([0.0, 0.0])
        self._f_gravity = np.array([0.0, 9.81 * self._mass])
        self._f_engine = np.array([0.0, 0.0])
        self._f_drag = np.array([0.0, 0.0])
        self._f_lift = np.array([0.0, 0.0])

        # Sprite info
        plane_pos = np.array(np.random.uniform(
            -plane_data["starting_config"]["position_px_deviation"], 
            plane_data["starting_config"]["position_px_deviation"],
            2
        )) + np.array(plane_data["starting_config"]["initial_position"])

        plane_size = np.array(plane_data["starting_config"]["size"])
        self.__reference_sprite = None
        self.sprite = None
        if use_gui:
            self.__reference_sprite = pygame.image.load(
                plane_data["sprite"]["side_view_dir"]
            )
            self.sprite = pygame.transform.scale(
                self.__reference_sprite,
                plane_size
            )
            # this sprite is used for reference, it is never displayed
            # it exists for rotation purposes only, as the entire
            # sprites gets compressed again and again otherwise
            self.__reference_sprite = pygame.transform.scale(
                self.__reference_sprite,
                plane_size
            )

            self.rect = self.__reference_sprite.get_rect(center=plane_pos)
        else:
            # if no gui, make custom rectangle instead
            self.rect = pygame.Rect(plane_pos - plane_size // 2, plane_size)

        self.bullet_data = plane_data["bullet_config"]
        self.bullets: List[Bullet] = []

    def tick(self, dt: float)-> None:
        """
        Update internal state of aircraft over given time interval.

        @params:
            - dt (float):
            Delta time over which changes need to be calculated.
        """

        # pitch unit vector
        self.pitch_uv[0] = math.cos(-math.pi / 180 * self._pitch)
        self.pitch_uv[1] = math.sin(-math.pi / 180 * self._pitch)

        # velocity unit vector
        if np.linalg.norm(self.v) != 0:
            self._v_uv = self.v / np.linalg.norm(self.v)

        # angle of attack
        self._AoA_deg = (
            math.atan2(self.pitch_uv[0], self.pitch_uv[1]) -
            math.atan2(self.v[0], self.v[1])
        ) * 180 / math.pi
        if self._AoA_deg > 180:
            self._AoA_deg -= 360
        elif self._AoA_deg < -180:
            self._AoA_deg += 360

        # engine force vector
        self._f_engine = \
            self.throttle * \
            0.1 * \
            self._engine_force * \
            self.pitch_uv

        # lift force vector
        coef_lift = self._lift_curve(self._AoA_deg)
        norm_lift = (
            self._const_lift *
            coef_lift *
            np.linalg.norm(self.v)**2
        )
        self._f_lift[0] = norm_lift * self._v_uv[1]
        self._f_lift[1] = norm_lift * -self._v_uv[0]

        # drag force vector
        coef_drag = (self._AoA_deg / (math.sqrt(40)))**2 + self._cd_min
        norm_drag = self._const_drag * coef_drag * np.linalg.norm(self.v) ** 2
        self._f_drag = -norm_drag * self._v_uv

        # resulting force vector, update velocity & position
        f_res = self._f_engine + self._f_gravity + self._f_drag + self._f_lift
        self.v += dt * f_res / self._mass 
        self.rect.center += self.v * dt
        # induced torque (close enough)
        if self._AoA_deg < self._AoA_crit_low[0]:
            self.adjust_pitch(norm_drag*0.0001*dt)
        if self._AoA_deg > self._AoA_crit_high[0]:
            self.adjust_pitch(-norm_drag*0.0001*dt)

        for bullet in self.bullets:
            bullet.update()        
        
    def adjust_pitch(self, dt: float)-> None:
        """
        Update pitch of aircraft over given time interval.

        @params:
            - dt (float): 
            Delta time over which changes need to be calculated.
        """
        self._pitch = (self._pitch + self._agility * dt) % 360
        if self.sprite:
            self.sprite = pygame.transform.rotate(
                self.__reference_sprite, 
                self._pitch
            )
            self.rect = self.sprite.get_rect(
                center=self.sprite.get_rect(center=self.rect.center).center
            )

    def _lift_curve(self, AoA: float)-> float:
        """
        Lift curve function based on critical angles and cl0

        @params:
            - AoA (float): Angle of attack.

        @returns:
            - float with lift coefficient at AoA
        """
        if AoA < self._AoA_crit_low[0] - 1:
            return 0.0
        elif self._AoA_crit_low[0] - 1 <= AoA < self._AoA_crit_low[0]:
            return self._AoA_crit_low[1] * abs(self._AoA_crit_low[0] - 1 - AoA)
        elif self._AoA_crit_low[0] <= AoA < 0.0:
            b = self._cl0 - self._AoA_crit_low[1]
            c = AoA / self._AoA_crit_low[0]
            return self._cl0 - b * c
        elif 0.0 <= AoA < self._AoA_crit_high[0]:
            b = self._AoA_crit_high[1] - self._cl0
            c = AoA / self._AoA_crit_high[0]
            return self._cl0 + b * c
        elif self._AoA_crit_high[0] <= AoA < self._AoA_crit_high[0] + 1:
            return self._AoA_crit_high[1] * abs(
                self._AoA_crit_high[0] - 1 - AoA
            )
        else:
            return 0
        
    def shoot(self)-> None:  
        """
        Shoots a bullet by adding a bullet object to the bullets list.
        """      
        # offset_x = self.rect.width // 2
        # offset_y = -self.rect.height // 2

        # bullet_x = self.rect.centerx + offset_x * \
        #     math.cos(math.radians(self._pitch)) - \
        #     offset_y * math.sin(math.radians(self._pitch))
        # bullet_y = self.rect.centery + offset_x * \
        #     math.sin(math.radians(self._pitch)) + \
        #     offset_y * math.cos(math.radians(self._pitch))
        
        self.bullets.append(
            Bullet(
                self.bullet_data,
                self.rect.center,
                self._pitch,
                bool(self.sprite)
            )
        )

# sources:
# https://github.com/gszabi99/War-Thunder-Datamine/tree/master/aces.vromfs.bin_u/gamedata/flightmodels
# https://en.wikipedia.org/wiki/Drag_curve
# https://www.grc.nasa.gov/www/k-12/VirtualAero/BottleRocket/airplane/lifteq.html
# https://www.grc.nasa.gov/www/k-12/VirtualAero/BottleRocket/airplane/drageq.html
# https://www.aerodynamics4students.com/aircraft-performance/drag-and-drag-coefficient.php
