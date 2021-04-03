import unittest

def generate_formula(n , edges):
    clause = []

    # Number of variables = n * n
    # i-th room can appear as 1st, 2nd ...nth position in Hamiltonian path
    for i in range(1, n + 1):
        # Each room appearing in Hamiltonian path.
        all_positions = [j for j in range(i * n - (n - 1), i * n + 1)]
        clause.append(all_positions)
        # No room can appear twice in the path
        for k in range(0, len(all_positions) - 1):
            clause.extend([[-1 * all_positions[k], -1 * all_positions[j + 1]] for j in range(k, len(all_positions) - 1)])
        # Every position is Hamiltonian path is occupied
        same_position = [j for j in range(i, n * (n - 1) + i + 1, n)]
        clause.append(same_position)
        # No two rooms occupy the same position
        for k in range(0, len(same_position) - 1):
            clause.extend([[-1 * same_position[k], -1 * same_position[j + 1]] for j in range(k, len(same_position) - 1)])

    # Nonadjacent nodes can't be adjacent in path
    adjacent_nodes = set()
    for e in edges:
        adjacent_nodes.add((e[0], e[1]))
        adjacent_nodes.add((e[1], e[0]))

    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            if (i, j) in adjacent_nodes: continue
            for k in range(0, n - 1):
                clause.append(list(map(lambda x: -1 * x, [(i - 1) * n + k + 1, (j  - 1) * n + k + 2])))
                clause.append(list(map(lambda x: -1 * x, [(j  - 1) * n + k + 1, (i - 1) * n + k + 2])))
    return clause


def printEquisatisfiableSatFormula(n , edges):
    clause = generate_formula(n, edges)
    print(len(clause), n * n)
    for i in range(0, len(clause)):
        print(' '.join(list(map(str, clause[i]))) + ' 0')

class TestHamiltonianPath(unittest.TestCase):
    def test_line_graph_for_hamiltonian_path(self):
        n = 4
        edges = [[1, 2], [2, 3], [3, 4]]
        #clauses = generate_formula(n, edges)
        printEquisatisfiableSatFormula(n ,edges)
