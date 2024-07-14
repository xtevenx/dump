from sage.all import *

from utils import *

if __name__ == '__main__':

    from pathlib import Path

    data = []

    for G in digraphs(5, augment='vertices'):

        if not G.is_connected() or G.is_bipartite():
            continue

        M = G.adjacency_matrix() * E(6)
        M = M + conjugate(M.transpose())
        P = SR(M.charpoly())

        if is_symmetric(P):
            data.append(G)

    save(Path(__file__).stem, data)
