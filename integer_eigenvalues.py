from sage.all import *

from utils import *

if __name__ == '__main__':

    from pathlib import Path

    data = []

    for G in digraphs(5, augment='vertices'):

        if not G.is_connected():
            continue

        M = G.adjacency_matrix() * E(6)
        M = M + conjugate(M.transpose())
        P = SR(M.charpoly())

        solutions = solve(P, var('x'), multiplicities=True)

        if all(s.right_hand_side().is_integer() for s in solutions[0]):
            data.append(G)

    save(Path(__file__).stem, data)
