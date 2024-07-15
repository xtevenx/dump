from os import makedirs

# jinja2 docs: https://jinja.palletsprojects.com/en/3.0.x/templates/
import jinja2

from sage.all import *


def get_charpoly(G):
    M = G.adjacency_matrix() * E(6)
    M = M + conjugate(M.transpose())
    return SR(M.charpoly())


def get_rank(P):
    return P.degree(var('x')) - min(tuple(zip(*P.coefficients()))[1])


def is_oriented(G):
    A = G.adjacency_matrix()
    return A.elementwise_product(A.transpose()) == 0


def is_symmetric(p):
    c = p.coefficients(sparse=False)

    i = 0
    while c[i] == 0:
        i = i + 1

    for j in range(i + 1, len(c), 2):
        if c[j] != 0:
            return False
    return True


DECIMAL_PRECISION = 8
RENDERED_IMAGES = 500
LIST_GRAPHS = 5


def save(location: str, graphs: list):
    makedirs(location, exist_ok=True)

    # WARN: change 999 to actual useful value (max smaller complete graph edges) if necessary.
    graphs.sort(key=lambda G: G.order() * 999 + G.size())

    summary = []
    output = []

    for id, G in enumerate(graphs):
        P = get_charpoly(G)
        S = solve(P, var('x'), multiplicities=True)
        S = [(s.right_hand_side(), m) for s, m in zip(*S)]

        radius = round(spectral_radius(P), DECIMAL_PRECISION)
        rank = get_rank(P)

        if not summary or summary[-1]['order'] < G.order():
            summary.append({
                'order': G.order(),
                'count': 1,
                'max_radius': radius,
                'max_radius_graphs': [id],
                'min_rank': rank,
                'min_rank_graphs': [id],
            })

        else:
            s = summary[-1]

            s['count'] += 1

            if radius > s['max_radius']:
                s['max_radius'] = radius
                s['max_radius_graphs'] = []
            if radius == s['max_radius']:
                s['max_radius_graphs'].append(id)

            if rank < s['min_rank']:
                s['min_rank'] = rank
                s['min_rank_graphs'] = []
            if rank == s['min_rank']:
                s['min_rank_graphs'].append(id)

        if id < RENDERED_IMAGES:
            fname = f'{location}/graph{id:03}.png'
            G.plot(layout='spring', iterations=9001).save(fname)

            output.append({
                'id': id,
                'fname': fname,
                'charpoly': latex(P),
                'radius': radius,
                'spec': latex(S)
            })

    for s in summary:
        for k, v in s.items():
            if k.endswith('_graphs'):
                if len(v) > LIST_GRAPHS:
                    s[k] = v[:LIST_GRAPHS] + ['...']

    with open('template.html') as fp:
        html = jinja2.Template(fp.read()).render(summary=summary, list=output)
    with open(f'{location}.html', 'w') as fp:
        fp.write(html)


def spectral_radius(p):
    rh = 0
    while True:
        try:
            rh = p.find_root(rh + 1e-8, p.degree(var('x')))
        except RuntimeError:
            break

    rl = 0
    while True:
        try:
            rl = p.find_root(-p.degree(var('x')), rl - 1e-8)
        except RuntimeError:
            break

    return max(-rl, rh)
