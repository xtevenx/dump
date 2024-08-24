"""
Requires the file https://users.cecs.anu.edu.au/~bdm/data/tourn6.txt to be
placed in the current directory. It contains all tournaments on 6 vertices,
prepared by Brendan McKay. Each is given as the upper triangle of the adjacency
matrix in row order, on one line without spaces.
"""

from sage.all import conjugate, matrix, var, E, Rational, SR

w = E(6)

with open('tourn6.txt') as fp:
    data = fp.read()

for line in data.strip().split('\n'):

    H = matrix(6)

    r = 0
    c = 1

    for e in line:

        if e == '1':
            H[r, c] = 1

        else:
            H[c, r] = 1

        c = c + 1
        if c >= 6:
            r = r + 1
            c = r + 1

    H = w * H + conjugate(w) * H.transpose()
    P = H.charpoly()

    # test if minimum eigenvalue strictly below -2

    # it suffices to find c <= -2 such that P(c) > 0, because P(-inf) = -inf.
    # we use rational c to prevent floating point imprecision.

    P = SR(P)

    c = 0
    while True:
        try:
            c = P.find_root(-P.degree(var('x')), c - 1e-12)
        except RuntimeError:
            break

    c = Rational(c + 1e-12)
    if not (c <= -2 and P(x=c) < 0):
        # didn't find a root below -2 !!

        # try solving the characteristic polynomial algebraically.
        for s in P.solve(var('x')):
            if bool(s.left_hand_side() == var('x')) and bool(s.right_hand_side() < -2):
                break
        else:
            # still didn't find a root below -2 !!!
            print(line, P)
