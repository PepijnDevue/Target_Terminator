import numpy as np


class Entities:
    """
    """
    
    def __init__(self):
        """
        scalars = [
            [mass, const_drag, const_lift, cl0, cd_min, engine_force, agility, throttle, pitch, AoA_deg, entity type flag, collision flag, coll radius],
            [0,    1,          2,          3,   4,      5,            6,       7,        8,     9,       10,               11,             12]
        ]

        vectors = [
            [AoA_crit_low, AoA_crit_high, v, pitch_uv, v_uv, f_gravity, f_engine, f_drag, f_lift, pos],
            [0,            1,             2, 3,        4,    5,         6,        7,      8,      9]
        ]
        """
        x = 1000 # dit is het max aantal objecten dat gespawnd kan worden. Miss iets met een config ofzo? 
        self.scalars = np.array(x, 12)

        y = 1000 # idem als x
        self.vectors = np.array(y, 9, 2) 
        pass

    def tick(self, actions: np.ndarray)-> None:
        """
        actions is een np array van [x, 2], met daarin pairs van PLANE_ID en nummers voor de verschillende acties, Bijv:
        [
            [2, 0],
            [3, 1],
        ]
        Hier doet plane met PLANE_ID 2 niks, en plane met PLANE_ID 3 adjust pitch omhoog.
        """
        pass

    def _adjust_pitch(self, deltas: np.ndarray)-> None:
        """
        deltas is een np array van [x, 2], met daarin pairs van ID en booleans met True als de plane omhoog adjust en False als de plane naar beneden adjust.
        """
        pass