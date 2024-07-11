import pygame
import math
import yaml
import time
import numpy as np

import utils


class Plane:
    """
    Plane class.

    + window_dimensions: (tuple[float, float]) dimensions of window
    + mass: (float) mass of aircraft, in kilogram (Kg).
    + engine_force: (float) constant force applied in direction
    of `pitch` in Newtons (N)
    + agility: (float) Degree to which the pitch can change,
    in degrees per delta.
    + c_drag: (float) 'constants' when calculating drag,
    such as air density and wing area
    + c_lift: (float) 'constants' when calculating lift,
    such as air density and wing area
    + AoA_crit_low: (tuple[float, float]) negative critical angle
     of attack in degrees and its corresponding lift coefficient
    + AoA_crit_high: (tuple[float, float]) positive critical angle
     of attack in degrees and its corresponding lift coefficient
    + cl0: (float) lift coefficient at AoA == 0
    + cd_min: (float) apex of drag curve; drag coefficient at AoA == 0
    + plane_size: (tuple[int, int]) dimensions of aircraft
    (length, height) in meter (m)
    + throttle: (float) throttle
    + pitch: (float) pitch in degrees
    + v: (tuple[float, float]) velocity vector
    + orientation: (int) direction of lift vector
    + flipstart: (float) timer for flip sprite
    + pos_virtual: (tuple[float, float]) aircraft position on screen
    + AoA_deg: (float) angle of attack in deg
    + pitch_uv: (tuple[float, float]) unitvector corresponding to
    `pitch`
    + v_uv: (tuple[float, float]) unitvector corresponding to `v`
    + f_gravity: (tuple[float, float]) gravity force vector
    + f_engine: (tuple[float, float]) engine force vector
    + f_drag: (tuple[float, float]) drag force vector
    + f_lift: (tuple[float, float]) drag force vector
    + sprite: (pygame.Surface) side view sprite
    + rot_sprite: (pygame.Surface) side view sprite, rotated
    + rot_rect: (pygame.Rect) rectangle object for pygame
    + flipsprite: (pygame.Surface) top view sprite
    + spritecontainer: (pygame.Surface) temp container for `flip()`
    """
    def __init__(
        self,
        plane_config: str,
        env_config: str,
    ) -> None:
        """
        
        """
        with open(plane_config, 'r') as stream:
            plane_data = yaml.safe_load(stream)
        assert utils.validate_plane_data(plane_data), "Invalid plane config."
        with open(env_config, 'r') as stream:
            env_data = yaml.safe_load(stream)
        assert utils.validate_env_data(env_data), "Invalid environment config."

        self.window_dimensions = env_data["window_dimensions"]

        # Constants
        self.mass = plane_data["properties"]["mass"]
        self.engine_force = plane_data["properties"]["engine_force"]
        self.agility = plane_data["properties"]["agility"]
        self.const_drag = plane_data["properties"]["drag_constant"]
        self.const_lift = plane_data["properties"]["lift_constant"]
        self.AoA_crit_low = plane_data["properties"]["critical_aoa_lower_bound"]
        self.AoA_crit_high = plane_data["properties"]["critical_aoa_higher_bound"]
        self.cl0 = plane_data["properties"]["lift_coeficient_aoa_0"]
        self.cd_min = plane_data["properties"]["drag_coeficient_aoa_0"]

        # Independent Variables
        self.throttle = plane_data["starting_config"]["initial_throttle"]
        self.pitch = plane_data["starting_config"]["initial_pitch"]
        self.v = np.array(plane_data["starting_config"]["initial_velocity"])
        self.orientation = 1
        self.flipstart = 0.0

        # Dependent variables (oa Numpy containers)
        self.AoA_deg = 0
        self.pitch_uv = np.array([0.0, 0.0])
        self.v_uv = np.array([0.0, 0.0])
        self.f_gravity = np.array([0.0, 9.81 * self.mass])
        self.f_engine = np.array([0.0, 0.0])
        self.f_drag = np.array([0.0, 0.0])
        self.f_lift = np.array([0.0, 0.0])

        # Sprite info
        plane_pos = \
            np.array(env_data["window_dimensions"]) * \
            np.array(plane_data["starting_config"]["initial_position"]) // \
            100
        plane_size = np.array(plane_data["starting_config"]["size"])
        self.sprite = None
        try:
            # Try and create sprites if in config
            self.sprite = pygame.image.load(
                plane_data["sprite"]["side_view_dir"]
            )
            self.flipsprite = pygame.image.load(
                plane_data["sprite"]["top_view_dir"]
            )

            # Scale sprites
            self.rot_sprite = pygame.transform.scale(
                self.sprite,
                plane_size
            )
            self.sprite = pygame.transform.scale(
                self.sprite,
                plane_size
            )
            self.flipsprite = pygame.transform.scale(self.flipsprite, plane_size)

            # For flipping or something, idk, ask Finn de Graaf
            self.spritecontainer = self.sprite

            # Get rectangle
            self.rot_rect = self.sprite.get_rect(center=plane_pos)
        except KeyError:
            # If sprites are not provided, make custom rectangle
            self.rot_rect = pygame.Rect(plane_pos - plane_size // 2, plane_size)

    def tick(self, dt: float) -> None:
        """
        Update internal state of aircraft over given time interval.

        :param dt: time since last frame (s) (float)
        :return: None
        """

        # pitch unit vector
        self.pitch_uv[0] = math.cos(-math.pi / 180 * self.pitch)
        self.pitch_uv[1] = math.sin(-math.pi / 180 * self.pitch)

        # velocity unit vector
        if np.linalg.norm(self.v) != 0:
            self.v_uv = self.v / np.linalg.norm(self.v)

        # angle of attack
        self.AoA_deg = (
            math.atan2(self.pitch_uv[0], self.pitch_uv[1]) -
            math.atan2(self.v[0], self.v[1])
        ) * 180 / math.pi
        if self.AoA_deg > 180:
            self.AoA_deg -= 360
        elif self.AoA_deg < -180:
            self.AoA_deg += 360

        # engine force vector
        self.f_engine = self.throttle * 0.1 * self.engine_force * self.pitch_uv

        # lift force vector
        coef_lift = self.lift_curve(self.orientation * self.AoA_deg)
        norm_lift = (
            self.const_lift *
            coef_lift *
            np.linalg.norm(self.v)**2 *
            self.orientation
        )
        self.f_lift[0] = norm_lift * self.v_uv[1]
        self.f_lift[1] = norm_lift * -self.v_uv[0]

        # drag force vector
        coef_drag = (self.AoA_deg / (math.sqrt(40)))**2 + self.cd_min
        norm_drag = self.const_drag * coef_drag * np.linalg.norm(self.v) ** 2
        self.f_drag = -norm_drag * self.v_uv

        # resulting force vector, update velocity & position
        f_res = self.f_engine + self.f_gravity + self.f_drag + self.f_lift
        self.v += dt * f_res / self.mass 
        self.rot_rect.center += self.v * dt
        # induced torque (close enough)
        if self.AoA_deg < self.AoA_crit_low[0]:
            self.adjust_pitch(norm_drag*0.0001*dt)
        if self.AoA_deg > self.AoA_crit_high[0]:
            self.adjust_pitch(-norm_drag*0.0001*dt)

        if self.sprite:
            self.flip_update_sprite()

    def adjust_pitch(self, dt: float):
        """
        Update pitch of aircraft over given time interval.

        :param dt: Delta time over which changes need to be calculated.
        :return: None
        """
        self.pitch = (self.pitch + self.agility * dt) % 360
        if self.sprite:
            self.rot_sprite = pygame.transform.rotate(self.sprite, self.pitch)
            self.rot_rect = self.rot_sprite.get_rect(
                center=self.sprite.get_rect(center=self.rot_rect.center).center
            )

    def flip(self):
        """
        Flips orientation of the aircraft and starts timer for
        `flipupdatesprite()`

        :return: None
        """
        if self.flipstart < 0.0000001:
            self.orientation = -self.orientation
        self.flipstart = time.time()

    def flip_update_sprite(self):
        """
        Updates aircraft sprite during orientation flip

        :return: None
        """
        if self.flipstart > 0.0000001:
            # show sprite after .25s
            if .25 < (time.time() - self.flipstart) < .5:
                self.sprite = self.flipsprite
            # reset sprite after .5s
            elif .5 <= (time.time() - self.flipstart):
                if self.orientation == 1:
                    self.sprite = self.spritecontainer
                else:
                    self.sprite = pygame.transform.flip(
                        self.spritecontainer, 
                        0, 
                        1
                    )
                self.flipstart = 0.0

        self.rot_sprite = pygame.transform.rotate(self.sprite, self.pitch)
        self.rot_rect = self.rot_sprite.get_rect(
            center=self.sprite.get_rect(center=self.rot_rect.center).center
        )

    def lift_curve(self, AoA: float):
        """
        Lift curve function based on critical angles and cl0

        :param AoA: angle of attack
        :return: lift coefficient at AoA
        """
        if AoA < self.AoA_crit_low[0] - 1:
            return 0.0
        elif self.AoA_crit_low[0] - 1 <= AoA < self.AoA_crit_low[0]:
            return self.AoA_crit_low[1] * abs(self.AoA_crit_low[0] - 1 - AoA)
        elif self.AoA_crit_low[0] <= AoA < 0.0:
            b = self.cl0 - self.AoA_crit_low[1]
            c = AoA / self.AoA_crit_low[0]
            return self.cl0 - b * c
        elif 0.0 <= AoA < self.AoA_crit_high[0]:
            b = self.AoA_crit_high[1] - self.cl0
            c = AoA / self.AoA_crit_high[0]
            return self.cl0 + b * c
        elif self.AoA_crit_high[0] <= AoA < self.AoA_crit_high[0] + 1:
            return self.AoA_crit_high[1] * abs(self.AoA_crit_high[0] - 1 - AoA)
        else:
            return 0

# sources:
# https://github.com/gszabi99/War-Thunder-Datamine/tree/master/aces.vromfs.bin_u/gamedata/flightmodels
# https://en.wikipedia.org/wiki/Drag_curve
# https://www.grc.nasa.gov/www/k-12/VirtualAero/BottleRocket/airplane/lifteq.html
# https://www.grc.nasa.gov/www/k-12/VirtualAero/BottleRocket/airplane/drageq.html
# https://www.aerodynamics4students.com/aircraft-performance/drag-and-drag-coefficient.php
