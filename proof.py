from sage.all import *

from utils import *

if __name__ == '__main__':

    from pathlib import Path

    data = [
        DiGraph([(0, 1), (1, 2), (2, 0), (0, 3)]),
        DiGraph([(0, 1), (1, 2), (2, 0), (0, 3), (1, 3)]),
        DiGraph([(0, 1), (1, 2), (2, 0), (0, 3), (3, 1)]),
        DiGraph([(0, 1), (1, 2), (2, 0), (3, 0), (1, 3)]),
        DiGraph([(0, 1), (1, 2), (2, 0), (0, 3), (1, 3), (3, 2)]),
        DiGraph([(0, 1), (1, 2), (2, 0), (0, 3), (1, 3), (2, 3), (0, 4), (1, 4), (2, 4), (0, 5),
                 (1, 5), (2, 5)]),
    ]

    save(Path(__file__).stem, data)
