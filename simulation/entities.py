import numpy as np

from simulation.airplanes import Airplanes
from simulation.targets import Targets

class Entities:
    def __init__(self, scalars, vectors, n_entities):
        self.scalars = np.ones((n_entities, scalars.shape[1]))
        self.vectors = np.ones((n_entities, vectors.shape[1], 2))

        self.scalars[:scalars.shape[0]] = scalars
        self.vectors[:vectors.shape[0]] = vectors
        n_planes = np.sum(scalars[:,11]==0)
        n_targets = np.sum(scalars[:,11]==1)

        self.airplanes = Airplanes(
            self.scalars[:n_planes],
            self.vectors[:n_planes]
        )
        self.targets = Targets(
            self.scalars[n_planes:n_planes+n_targets],
            self.vectors[n_planes:n_planes+n_targets]
        )

    def tick(self, dt, actions):
        self.airplanes.tick(dt, actions)  # voor als je non-airplane agents wilt toevoegen: actions -> actions[:n_planes]
        # TODO: collision
        # TODO: bullets


