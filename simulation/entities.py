import numpy as np
import time

from simulation.airplanes import Airplanes
from simulation.targets import Targets
from simulation.bullets import Bullets


class Entities:
    def __init__(self, scalars, vectors, n_entities, boundaries):
        self.scalars = np.zeros((n_entities, scalars.shape[1]))
        self.vectors = np.zeros((n_entities, vectors.shape[1], 2))
        self.scalars[:,11] = -1
        self.scalars[:,12] = -1

        self.scalars[:scalars.shape[0]] = scalars
        self.vectors[:vectors.shape[0]] = vectors
        self.boundaries = boundaries  # boundaries heeft het format [[domein_x],[domein_y]], dus bijv. [[0,1280],[0,720]]

        self.n_planes = np.sum(scalars[:,11]==0)
        self.n_targets = np.sum(scalars[:,11]==1)
        self.n_bullets = 0
        self.n_total = self.n_planes + self.n_targets

        self.airplanes = Airplanes(
            self.scalars[:self.n_planes],
            self.vectors[:self.n_planes]
        )
        self.targets = Targets(
            self.scalars[self.n_planes:self.n_planes+self.n_targets],
            self.vectors[self.n_planes:self.n_planes+self.n_targets]
        )
        self.bullets = Bullets(
            self.scalars[self.n_planes + self.n_targets:],
            self.vectors[self.n_planes + self.n_targets:]
        )

    def tick(self, dt, actions):
        self.airplanes.tick(dt, actions)
        self.bullets.tick(dt)
        # voor als je non-airplane agents wilt toevoegen: actions -> actions[:n_planes] oid
        #  vooralsnog ga ik er van uit dat alle agents vliegtuigen zijn

        self.entity_collision()

        shoot_id = actions[actions[:, 1] == 5]
        if shoot_id.shape[0]!=0:
            self.spawn_bullet(dt, shoot_id[:,0])
        self.n_total += self.bullets.despawn()

        # TODO: `tick` uitvoeren op *alleen* die rijen die 'levend' zijn, kan
        #  wellicht sneller zijn, het kan echter ook dat het slicen/masken meer
        #  tijd kost dan de overbodige berekeningen

    def spawn_bullet(self, dt, id):
        # TODO: firerate?
        pos = self.vectors[id,3] + self.vectors[id,4] * (self.scalars[id,9][:,None] + 2)  # `2` = afstand tussen center van bullet en rand hitbox van vliegtuig in m
        v = self.vectors[id,2] + (100 * self.vectors[id,4])  # `100` = v van bullet relatief aan vliegtuig in m/s
        vectors = np.zeros((id.shape[0], self.vectors.shape[1], 2))
        vectors[:,3] = pos
        vectors[:,2] = v
        self.n_bullets += id.shape[0]
        self.n_total += id.shape[0]
        self.bullets.spawn(vectors)

    def entity_collision(self):
        # `entity_collision` gaat er van uit dat alle hitboxen 'rond' zijn, dit is
        #  natuurlijk niet realistisch maar maakt het wel aanzienlijk veel
        #  sneller te berekenen, en op hoge snelheden maakt een exacte hitbox
        #  toch niet super veel uit
        vectors = self.vectors[(self.scalars[:,11] != -1) & (self.scalars[:,12] == -1)]
        scalars = self.scalars[(self.scalars[:,11] != -1) & (self.scalars[:,12] == -1)]

        positions = vectors[:, 3]
        d_curr = np.linalg.norm(positions[:, np.newaxis] - positions, axis=2)

        radii = scalars[:, 9]
        d_min = radii[:, np.newaxis] + radii
        np.fill_diagonal(d_min, -1)

        d = d_curr - d_min
        i = np.argsort(d, axis=1)
        mask = np.min(d, axis=1) < 0
        coll_indices = np.where(mask, i[:, 0], -1)

        coll_entity_types = np.where(coll_indices != -1, scalars[coll_indices, 11], -1)

        # dit is helemaal kut
        in_bounds = (positions[:, 0] <= self.boundaries[0, 0]) | (
                    positions[:, 0] >= self.boundaries[0, 1]) | (positions[:, 1] <= self.boundaries[1, 0]) | (
                    positions[:, 1] >= self.boundaries[1, 1])

        coll_entity_types = np.where(in_bounds, 3, coll_entity_types)

        self.scalars[(self.scalars[:,11] != -1) & (self.scalars[:,12] == -1), 12] += (coll_entity_types + 1)
