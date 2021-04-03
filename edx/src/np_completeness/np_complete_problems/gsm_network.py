import unittest
from math import factorial
# python3
# Graph coloring problem - Generates formula for minisat solvers
#
#n, m = map(int, input().split())
#edges = [ list(map(int, input().split())) for i in range(m) ]

class GraphNode:
    def __init__(self, i):
        self.red, self.blue, self.green  = 3 * i - 2, 3 * i - 1, 3 * i

def generate_formula(n, edges):
    clause = []
    for i in range(1, n + 1):
        node = GraphNode(i)
        # Every node needs to have a color
        clause.append([node.red, node.blue, node.green])
        # Every node can have one color only
        clause.append([-node.red, -node.green])
        clause.append([-node.red, -node.blue])
        clause.append([-node.blue, -node.green])

    # Adjacent nodes can't have same color
    for e in edges:
        u = GraphNode(e[0])
        v = GraphNode(e[1])
        clause.append([-u.red, -v.red])
        clause.append([-u.blue, -v.blue])
        clause.append([-u.green, -v.green])
    return clause

def printEquisatisfiableSatFormula(n, edges):
    clause = generate_formula(n, edges)
    print(len(clause), n * 3)
    for i in range(0, len(clause)):
        print(' '.join(list(map(str, clause[i]))), 0)

class TestGraphColoring(unittest.TestCase):
    def test_triangle_for_coloring(self):
        n = 3
        edges = [[1, 2], [1, 3], [2, 3]]
        clauses = generate_formula(n, edges)
        expected_clause_count = n + n * (factorial(3) / factorial(2)) + len(edges) * (factorial(3) / factorial(2))
        assert len(clauses) == expected_clause_count

    def test_graph_with_six_nodes_for_coloring(self):
        n = 6
        edges = [[1, 2], [1, 3], [1, 4], [2, 3], [2, 5], [3, 4], [3, 6], [5, 6]]
        clauses = generate_formula(n, edges)
        expected_clause_count = n + n * (factorial(3) / factorial(2)) + len(edges) * (factorial(3) / factorial(2))
        assert len(clauses) == expected_clause_count

if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)