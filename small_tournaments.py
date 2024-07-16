from sage.all import *

from utils import *

if __name__ == '__main__':

    from pathlib import Path

    data = []

    for G in digraphs(8, property=lambda g: g.is_tournament(), augment='vertices'):
        data.append(G)

    save(Path(__file__).stem, data)
