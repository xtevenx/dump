from os import makedirs
from time import monotonic

# jinja2 docs: https://jinja.palletsprojects.com/en/3.0.x/templates/
import jinja2

from sage.all import *


def count_distinct_roots(P):
    return P.degree(var('x')) - (P.gcd(P.derivative())).degree(var('x'))


def count_integer_roots(P):
    return sum(bool(P(x=c) == 0) for c in range(-P.degree(var('x')), P.degree(var('x')) + 1))


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


DISPLAY_PRECISION = 4
RENDER_GRAPHS = 200
LIST_GRAPHS = 5


def save(location: str, graphs: list):
    start_time = monotonic()

    makedirs(location, exist_ok=True)

    # WARN: change 999 to actual useful value (max smaller complete graph edges) if necessary.
    graphs.sort(key=lambda G: G.order() * 999 + G.size())

    summary = []
    output = []

    for id, G in enumerate(graphs):
        P = get_charpoly(G)

        max_lambda = round(max_eigenvalue(P), DISPLAY_PRECISION)
        min_lambda = round(min_eigenvalue(P), DISPLAY_PRECISION)
        rank = get_rank(P)

        if not summary or summary[-1]['order'] < G.order():
            summary.append({
                'order': G.order(),
                'count': 1,
                'max_max_lambda': max_lambda,
                'max_max_lambda_graphs': [id],
                'min_max_lambda': max_lambda,
                'min_max_lambda_graphs': [id],
                'max_min_lambda': min_lambda,
                'max_min_lambda_graphs': [id],
                'min_min_lambda': min_lambda,
                'min_min_lambda_graphs': [id],
                'min_rank': rank,
                'min_rank_graphs': [id],
            })

        else:
            s = summary[-1]

            s['count'] += 1

            if max_lambda > s['max_max_lambda']:
                s['max_max_lambda'] = max_lambda
                s['max_max_lambda_graphs'] = []
            if max_lambda == s['max_max_lambda']:
                s['max_max_lambda_graphs'].append(id)

            if max_lambda < s['min_max_lambda']:
                s['min_max_lambda'] = max_lambda
                s['min_max_lambda_graphs'] = []
            if max_lambda == s['min_max_lambda']:
                s['min_max_lambda_graphs'].append(id)

            if min_lambda > s['max_min_lambda']:
                s['max_min_lambda'] = min_lambda
                s['max_min_lambda_graphs'] = []
            if min_lambda == s['max_min_lambda']:
                s['max_min_lambda_graphs'].append(id)

            if min_lambda < s['min_min_lambda']:
                s['min_min_lambda'] = min_lambda
                s['min_min_lambda_graphs'] = []
            if min_lambda == s['min_min_lambda']:
                s['min_min_lambda_graphs'].append(id)

            if rank < s['min_rank']:
                s['min_rank'] = rank
                s['min_rank_graphs'] = []
            if rank == s['min_rank']:
                s['min_rank_graphs'].append(id)

        output.append({
            '__charpoly': P,
            'id': id,
            'fname': f'{location}/graph{id:06}.png',
            'charpoly': latex(P),
            'max_lambda': max_lambda,
            'min_lambda': min_lambda,
        })

    print(f'[{location}] Searched ({monotonic() - start_time:.1f} seconds)')

    ensure_render = set()
    for s in summary:
        for k, v in s.items():
            if k.endswith('_graphs'):
                if len(v) > LIST_GRAPHS:
                    s[k] = v[:LIST_GRAPHS] + ['...']
                ensure_render = ensure_render.union(s[k])

    for i in range(len(output) - 1, -1, -1):
        D = output[i]
        if D['id'] < RENDER_GRAPHS or D['id'] in ensure_render:
            S = solve(D['__charpoly'], var('x'), multiplicities=True)
            S = [(s.right_hand_side(), m) for s, m in zip(*S)]
            D['spec'] = latex(S)
            graphs[i].plot(layout='spring', iterations=9001).save(D['fname'])
        else:
            output.pop(i)

    print(f'[{location}] Rendered ({monotonic() - start_time:.1f} seconds)')

    with open('template.html') as fp:
        html = jinja2.Template(fp.read()).render(summary=summary, list=output)
    with open(f'{location}.html', 'w') as fp:
        fp.write(html)

    print(f'[{location}] Done ({monotonic() - start_time:.1f} seconds)')


# def max_eigenvalue(p):
#     x = 0
#     while True:
#         try:
#             x = p.find_root(x + 1e-12, p.degree(var('x')))
#         except RuntimeError:
#             return x

# def min_eigenvalue(p):
#     x = 0
#     while True:
#         try:
#             x = p.find_root(-p.degree(var('x')), x - 1e-12)
#         except RuntimeError:
#             return x


def max_eigenvalue(p):
    if p == 1:
        return 0

    orig = p

    guesses = [0]
    while p:
        while True:
            try:
                guesses.append(p.find_root(guesses[-1] + 1e-12, p.degree(var('x'))))
            except RuntimeError:
                break
        p = p.derivative(var('x'))

    for x in reversed(guesses):
        if abs(orig(x=x)) < 1e-4:
            return x


def min_eigenvalue(p):
    if p == 1:
        return 0

    orig = p

    guesses = [0]
    while p:
        while True:
            try:
                guesses.append(p.find_root(-p.degree(var('x')), guesses[-1] - 1e-12))
            except RuntimeError:
                break
        p = p.derivative(var('x'))

    for x in reversed(guesses):
        if abs(orig(x=x)) < 1e-4:
            return x
