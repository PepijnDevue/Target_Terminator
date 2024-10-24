import time
import numpy as np
from tqdm import tqdm
import random

dt = 1/60
l = [0,1,2,3,4,5]

def run(entities):
    t = time.time()
    for _ in tqdm(range(100000)):
        for _ in range(100000):
            a = random.choice(l)
            actions = np.array([[0,a]])

            entities.tick(dt,actions)
            if(entities.scalars[0,12] != -1):
                break

    print(time.time()-t)
