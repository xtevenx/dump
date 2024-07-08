from os import makedirs

from sage.all import *

from utils import enumerate_graphs, spectral_radius


def save(location: str, order: int) -> list:
    info = []

    for graph in enumerate_graphs(order):
        G = DiGraph(graph)

        if not G.is_tournament():
            continue

        M = G.adjacency_matrix() * E(6)
        M = M + conjugate(M.transpose())
        P = SR(M.charpoly())

        id = len(info) + 1
        fname = f'{location}/graph{id:03}.png'
        print(f'Saving image {fname}')
        G.plot(layout='spring', iterations=9001).save(fname)

        solutions = solve(P, var('x'), multiplicities=True)
        solutions = [(s.right_hand_side(), m) for s, m in zip(*solutions)]

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

    data = save(FNAME, order=6)

    with open(f'template.html') as fp:
        html = jinja2.Template(fp.read()).render(list=data)
        with open(f'{FNAME}.html', 'w') as fp:
            fp.write(html)
