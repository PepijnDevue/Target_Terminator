import numpy as np

class Bullets:
    def __init__(self, scalars, vectors):
        self.scalars = scalars
        self.vectors = vectors
        self.n_bullets = 0

    def tick(self, dt):
        self.vectors[:, 3] += dt * self.vectors[:, 2]
        # self.vectors[:self.n_bullets, 3] += dt * self.vectors[:self.n_bullets, 2]

        # TODO: het is me zo niet duidelijk of het sneller is om *alle* rijen
        #  gereserveerd voor bullets, dan wel niet in gebruik, te updateten, of
        #  dat het sneller is eerst n_bullets te updateten en vervolgens
        #  *alleen* de rijen met bestaande bullets te updateten. als dit tweede
        #  het geval is gebruiken we dus (de weg-gecommentete) line 9 ipv 8

    def spawn(self, vectors):
        # TODO: dit is nog niet getest ik heb geen idee of dit werkt
        scalars = np.zeros((vectors.shape[0], self.scalars.shape[1]))
        scalars[:,11] = 2
        scalars[:,12] = -1
        i = np.argsort(self.scalars[:,11])[:scalars.shape[0]]
        self.scalars[i] = scalars
        self.vectors[i] = vectors

    def despawn(self):
        pass

