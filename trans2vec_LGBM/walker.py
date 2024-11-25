import numpy as np
import scipy.sparse as sp
from numba import njit


@njit
def random_choice(arr, p):
    """Similar to `numpy.random.choice` and it suppors p=option in numba.
    refer to <https://github.com/numba/numba/issues/2539#issuecomment-507306369>

    Parameters
    ----------
    arr : 1-D array-like
    p : 1-D array-like
        The probabilities associated with each entry in arr

    Returns
    -------
    sample : ndarray with 1 element
        The generated random sample
    """
    return arr[np.searchsorted(np.cumsum(p), np.random.random(), side="right")]


class BiasedRandomWalker:
    """Biased second order random walks in Node2Vec.

    Parameters:
    -----------
    walk_number (int): Number of random walks. Default is 10.
    walk_length (int): Length of random walks. Default is 80.
    p (float): Return parameter (1/p transition probability) to move towards from previous node.
    q (float): In-out parameter (1/q transition probability) to move away from previous node.
    """

    def __init__(self, walk_length: int = 80,
                 walk_number: int = 10,
                 p: float = 0.5,
                 q: float = 0.5):
        self.walk_length = walk_length
        self.walk_number = walk_number
        try:
            _ = 1 / p
        except ZeroDivisionError:
            raise ValueError("The value of p is too small or zero to be used in 1/p.")
        self.p = p
        try:
            _ = 1 / q
        except ZeroDivisionError:
            raise ValueError("The value of q is too small or zero to be used in 1/q.")
        self.q = q

    def walk(self, graph: sp.csr_matrix):
        data = graph.data
        indices = graph.indices
        indptr = graph.indptr
        walk_length = self.walk_length
        walk_number = self.walk_number

        @njit(nogil=False)
        def random_walk():
            N = len(indptr) - 1
            for _ in range(walk_number):
                nodes = np.arange(N, dtype=np.int32)
                np.random.shuffle(nodes)
                for n in nodes:
                    walk = [n]
                    current_node = n
                    for _ in range(walk_length - 1):
                        neighbors = indices[indptr[current_node]:indptr[current_node + 1]]
                        if neighbors.size == 0:
                            break

                        probability = data[indptr[current_node]: indptr[current_node + 1]].copy()
                        norm_probability = probability / np.sum(probability)
                        current_node = random_choice(neighbors, norm_probability)
                        walk.append(current_node)
                    yield walk

        walks = [list(map(str, walk)) for walk in random_walk()]
        return walks