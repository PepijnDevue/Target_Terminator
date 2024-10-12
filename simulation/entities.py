import numpy as np

from simulation.airplanes import Airplanes
from simulation.targets import Targets

class Entities:
    def __init__(self, scalars, vectors, n_entities):
        self.scalars = np.ones((n_entities, scalars.shape[1]))
        self.vectors = np.ones((n_entities, vectors.shape[1], 2))

        self.scalars[:scalars.shape[0]] = scalars
        self.vectors[:vectors.shape[0]] = vectors
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

    def tick(self, dt, actions):
        self.airplanes.tick(dt, actions)  # voor als je non-airplane agents wilt toevoegen: actions -> actions[:n_planes]
        self.collision()
        # TODO: bullets

    def collision(self):
        M = np.tile(self.vectors[:self.n_total, 3], (self.n_total, 1, 1))
        d_curr = np.linalg.norm((M - np.transpose(M, (1, 0, 2))), axis=2)

        N = np.tile(self.scalars[:self.n_total, 9], (self.n_total, 1))
        d_min = (N+N.T)
        np.fill_diagonal(d_min, -99999999)
        d = d_curr-d_min
        i = np.argsort(d)

        mask = np.sort(d)[:,0] < 0
        coll_indices = mask * i[:,0] + mask - 1
        mask2 = self.scalars[:self.n_total,12] == -1
        self.scalars[:self.n_total, 12] += mask2 * (coll_indices+1)
