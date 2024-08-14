"""
Requires the file https://users.cecs.anu.edu.au/~bdm/data/rt11.txt to be placed
in the current directory. It contains all regular tournaments on 11 vertices,
prepared by Brendan McKay. Each is given as the upper triangle of the adjacency
matrix in row order, on one line without spaces.
"""

from sage.all import conjugate, matrix, E

w = E(6)

with open('rt11.txt') as fp:
    data = fp.read()

for line in data.strip().split('\n'):

    H = matrix(11, 11)

    r = 0
    c = 1

    for e in line:

        if e == '1':
            H[r, c] = 1

        else:
            H[c, r] = 1

        c = c + 1
        if c >= 11:
            r = r + 1
            c = r + 1

    H = w * H + conjugate(w) * H.transpose()
    P = H.charpoly()

    for i, c in enumerate(P.coefficients(sparse=False)):
        if i % 2 == 0 and c != 0:
            break
    else:
        # has symmetric spectrum !!
        print(line, P)
