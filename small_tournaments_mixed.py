from sage.all import *

from utils import *

if __name__ == '__main__':

    from pathlib import Path

    data = []

    for G in digraphs(5, property=lambda g: g.to_undirected().is_clique(), augment='vertices'):
        data.append(G)

    save(Path(__file__).stem, data)
