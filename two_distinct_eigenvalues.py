from sage.all import *

from utils import enumerate_graphs


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

        if G.is_bipartite():
            continue

        if oriented_only:
            A = G.adjacency_matrix()
            if A.elementwise_product(A.transpose()) != 0:
                continue

        M = G.adjacency_matrix() * E(6)
        M = M + conjugate(M.transpose())
        P = M.charpoly()

        solutions = solve(SR(P), var('x'), multiplicities=True)

        if len(solutions[0]) == 2:
            fname = f'{location}/graph{len(info):03}.png'
            print(f'Saving image {fname}')
            G.plot(layout='spring', iterations=9001).save(fname)

            solutions = [(s.right_hand_side(), m) for s, m in zip(*solutions)]
            solutions.sort(key=lambda t: t[0])

            info.append({'fname': fname, 'charpoly': latex(P), 'spec': latex(solutions)})

    return info


if __name__ == '__main__':
    # jinja2 docs: https://jinja.palletsprojects.com/en/3.0.x/templates/

    import jinja2

    from pathlib import Path

    FNAME = Path(__file__).stem

    data = save(FNAME, order=5)

    with open(f'template.html') as fp:
        html = jinja2.Template(fp.read()).render(list=data)
        with open(f'{FNAME}.html', 'w') as fp:
            fp.write(html)
