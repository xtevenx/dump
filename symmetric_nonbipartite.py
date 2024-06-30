# Copied fromDavid Eisenstat https://stackoverflow.com/a/71701505
# using license CC BY-SA 4.0 https://creativecommons.org/licenses/by-sa/4.0/

import itertools


# Returns labels approximating the orbits of graph. Two nodes in the same orbit
# have the same label, but two nodes in different orbits don't necessarily have
# different labels.
def invariant_labels(graph, n):
    labels = [1] * n
    for _ in range(2):
        incoming = [0] * n
        outgoing = [0] * n
        for i, j in graph:
            incoming[j] += labels[i]
            outgoing[i] += labels[j]
        for i in range(n):
            labels[i] = hash((incoming[i], outgoing[i]))
    return labels


# Returns the inverse of perm.
def inverse_permutation(perm):
    n = len(perm)
    inverse = [None] * n
    for i in range(n):
        inverse[perm[i]] = i
    return inverse


# Returns the permutation that sorts by label.
def label_sorting_permutation(labels):
    n = len(labels)
    return inverse_permutation(sorted(range(n), key=lambda i: labels[i]))


# Returns the graph where node i becomes perm[i] .
def permuted_graph(perm, graph):
    perm_graph = [(perm[i], perm[j]) for (i, j) in graph]
    perm_graph.sort()
    return perm_graph


# Yields each permutation generated by swaps of two consecutive nodes with the
# same label.
def label_stabilizer(labels):
    n = len(labels)
    factors = (itertools.permutations(block)
               for (_, block) in itertools.groupby(range(n), key=lambda i: labels[i]))
    for subperms in itertools.product(*factors):
        yield [i for subperm in subperms for i in subperm]


# Returns the canonical labeled graph isomorphic to graph.
def canonical_graph(graph, n):
    labels = invariant_labels(graph, n)
    sorting_perm = label_sorting_permutation(labels)
    graph = permuted_graph(sorting_perm, graph)
    labels.sort()
    return max((permuted_graph(perm, graph), perm[sorting_perm[n - 1]])
               for perm in label_stabilizer(labels))


# Returns the list of permutations that stabilize graph.
def graph_stabilizer(graph, n):
    return [
        perm for perm in label_stabilizer(invariant_labels(graph, n))
        if permuted_graph(perm, graph) == graph
    ]


# Yields the subsets of range(n) .
def power_set(n):
    for r in range(n + 1):
        for s in itertools.combinations(range(n), r):
            yield list(s)


# Returns the set where i becomes perm[i] .
def permuted_set(perm, s):
    perm_s = [perm[i] for i in s]
    perm_s.sort()
    return perm_s


# If s is canonical, returns the list of permutations in group that stabilize s.
# Otherwise, returns None.
def set_stabilizer(s, group):
    stabilizer = []
    for perm in group:
        perm_s = permuted_set(perm, s)
        if perm_s < s:
            return None
        if perm_s == s:
            stabilizer.append(perm)
    return stabilizer


# Yields one representative of each isomorphism class.
def enumerate_graphs(n):
    assert 0 <= n
    if 0 == n:
        yield []
        return
    for subgraph in enumerate_graphs(n - 1):
        sub_stab = graph_stabilizer(subgraph, n - 1)
        for incoming in power_set(n - 1):
            in_stab = set_stabilizer(incoming, sub_stab)
            if not in_stab:
                continue
            for outgoing in power_set(n - 1):
                out_stab = set_stabilizer(outgoing, in_stab)
                if not out_stab:
                    continue
                graph, i_star = canonical_graph(
                    subgraph + [(i, n - 1) for i in incoming] + [(n - 1, j) for j in outgoing],
                    n,
                )
                if i_star == n - 1:
                    yield graph


from sage.all import *


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

        if is_symmetric(P):
            fname = f"{location}/graph{len(info):03}.png"
            print(f"Saving image {fname}.")
            G.plot(layout='spring', iterations=9001).save(fname)

            try:
                solutions = solve(SR(P), var('x'), multiplicities=True)
                solutions = [(s.right_hand_side(), m) for s, m in zip(*solutions)]
                solutions.sort(key=lambda t: t[0])
            except NotImplementedError:
                solutions = "Unknown"

            info.append({"fname": fname, "charpoly": latex(P), "spec": latex(solutions)})

    return info


def generate() -> list:
    return save("symmetric_nonbipartite", order=5)


if __name__ == "__main__":
    # jinja2 docs: https://jinja.palletsprojects.com/en/3.0.x/templates/

    import jinja2

    with open('symmetric_nonbipartite.template') as fp:
        html = jinja2.Template(fp.read()).render(list=generate())
        with open('symmetric_nonbipartite.html', 'w') as fp:
            fp.write(html)
