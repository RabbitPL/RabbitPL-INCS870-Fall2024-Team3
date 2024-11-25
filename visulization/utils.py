import random
import numpy as np
from numba import njit, jit


@njit
def numba_seed(sd):
    np.random.seed(sd)


def random_seed(seed=None):
    np.random.seed(seed)
    numba_seed(seed)
    random.seed(seed)


@jit(cache=True, nopython=True)
def normalized_probs(unnormalized_probs):
    if len(unnormalized_probs) > 0:
        normalized_probs = unnormalized_probs / unnormalized_probs.sum()
    return normalized_probs


@jit(cache=True, nopython=True)
def combine_probs(p1, p2, alpha):
    probs1 = normalized_probs(p1)
    probs2 = normalized_probs(p2)

    assert len(probs1) == len(probs2), "combine_probs invalid"
    combine_probs = np.multiply(np.power(probs1, alpha), np.power(probs2, 1 - alpha))
    return combine_probs


def load_labels(filename):
    fin = open(filename, 'r')
    labels = {}
    while 1:
        l = fin.readline()
        if l == '':
            break
        vec = l.strip().split(' ')
        node = str(int(vec[0]) - 1)
        labels[node] = int(vec[1])
    fin.close()
    return labels