from sage.all import *

from utils import *

if __name__ == '__main__':

    from pathlib import Path

    data = []

    for n in range(6):

        with open(f'data/orient{n+1}.d6') as fp:
            s = fp.read()

        for line in s.strip().split('\n'):
            G = DiGraph(line.lstrip('&'), format='dig6')

            if not G.is_connected():
                continue

            M = G.adjacency_matrix() * E(6)
            M = M + conjugate(M.transpose())
            P = SR(M.charpoly())

            if count_distinct_roots(P) == 2:
                data.append(G)

    save(Path(__file__).stem, data)
