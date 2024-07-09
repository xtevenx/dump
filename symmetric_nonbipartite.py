from os import makedirs

from sage.all import *

from utils import enumerate_graphs, spectral_radius


def is_symmetric(p):
    c = p.coefficients(sparse=False)

    i = 0
    while c[i] == 0:
        i = i + 1

    for j in range(i + 1, len(c), 2):
        if c[j] != 0:
            return False
    return True


def save(location: str, order: int, oriented_only: bool = False) -> list:
    info = []

    for graph in enumerate_graphs(order):
        G = DiGraph(graph)

        if not G.is_connected():
            continue

        if G.is_bipartite():
            continue

        if oriented_only:
            A = G.adjacency_matrix()
            if A.elementwise_product(A.transpose()) != 0:
                continue

        M = G.adjacency_matrix() * E(6)
        M = M + conjugate(M.transpose())
        P = SR(M.charpoly())

        if is_symmetric(P):
            id = len(info) + 1
            fname = f'{location}/graph{id:03}.png'
            print(f'Saving image {fname}')
            G.plot(layout='spring', iterations=9001).save(fname)

            try:
                solutions = solve(SR(P), var('x'), multiplicities=True)
                solutions = [(s.right_hand_side(), m) for s, m in zip(*solutions)]
                solutions.sort(key=lambda t: t[0])
            except NotImplementedError:
                solutions = 'Unknown'

            info.append({
                'fname': fname,
                'id': id,
                'charpoly': latex(P),
                'r': spectral_radius(P),
                'spec': latex(solutions)
            })

    return info


if __name__ == '__main__':
    # jinja2 docs: https://jinja.palletsprojects.com/en/3.0.x/templates/

    import jinja2

    from pathlib import Path

    FNAME = Path(__file__).stem

    makedirs(FNAME, exist_ok=True)

    data = save(FNAME, order=5)

    with open(f'template.html') as fp:
        html = jinja2.Template(fp.read()).render(list=data)
        with open(f'{FNAME}.html', 'w') as fp:
            fp.write(html)
