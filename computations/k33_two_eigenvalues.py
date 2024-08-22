"""There are 12 orientations of K33 with two distinct eigenvalues."""

from networkx import complete_bipartite_graph
from sage.all import conjugate, sqrt, var, E, Graph

w = E(6)

x = var('x')
target = (x + sqrt(3))**3 * (x - sqrt(3))**3

cnt = 0
for G in Graph(complete_bipartite_graph(3, 3)).orientations():

    H = G.adjacency_matrix()
    H = w * H + conjugate(w) * H.transpose()
    P = H.charpoly()

    # test if -sqrt(3) is an eigenvalue

    if P == target:
        cnt = cnt + 1

print(f'Found {cnt} orientations.')
