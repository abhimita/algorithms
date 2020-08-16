import collections
import networkx as nx
import math
import unittest
import sys

sys.setrecursionlimit(1500)

def all_permutations(k):
    if k == 1:
        return ['0', '1']
    else:
        return list(map(lambda x: str(0) + x, all_permutations(k - 1))) + \
               list(map(lambda x: str(1) + x, all_permutations(k - 1)))

def draw_k_universal_graph(k):
    G = nx.MultiDiGraph()
    for p in all_permutations(k):
        src =  p[0: k - 1]
        dest = p[1:]
        G.add_edge(src, dest)
    nx.nx_pydot.write_dot(G, '%dmer-graph.dot' % k)

def build_debruijn_graph(patterns):
    vertices = set()
    adj_list = collections.defaultdict(list)
    out_degree = collections.defaultdict(lambda: 0)
    in_degree = collections.defaultdict(lambda: 0)
    for p in patterns:
        src = p[0: k - 1]
        dest = p[1:]
        adj_list[src].append(dest)
        in_degree[dest] += 1
        out_degree[src] += 1
        vertices.add(src)
        vertices.add(dest)
    start_node = list(vertices)[0]
    return adj_list, vertices, start_node

def k_universal(k):
    if k == 1:
        return '01'
    patterns = all_permutations(k)
    adj_list, vertices, start_node = build_debruijn_graph(patterns)
    vertices_in_path = []

    def traverse(start_node):
        while len(adj_list[start_node]) > 0:
            nbr = adj_list[start_node].pop(0)
            traverse(nbr)
        vertices_in_path.append(start_node)
        return vertices_in_path
    vertices_in_path = traverse(start_node)
    assert all([len(adj_list[k]) == 0 for k in adj_list.keys()])
    vertices_in_path.reverse()
    result = ''.join([v if i == 0 else v[-1] for i, v in enumerate(vertices_in_path)])[: -1 * (k - 1)]
    return result

class TestUniversalString(unittest.TestCase):
    def get_expected_result(self, universal_string, k):
        all_kmers = []
        for i in range(len(universal_string)):
            end_pos = i + k
            if end_pos >= len(universal_string):
                kmer = universal_string[i : len(universal_string)] + universal_string[0 : k - len(universal_string[i : len(universal_string)])]
            else:
                kmer = universal_string[i : i + k]
            all_kmers.append(kmer)
        expected = sorted(all_permutations(k))
        sorted_kmers = sorted(all_kmers)
        return expected, sorted_kmers

    def test_for_1_mer(self):
        k = 1
        universal_string = k_universal(k)
        assert len(universal_string) == int(math.pow(2, k))
        expected, actual = self.get_expected_result(universal_string, k)
        assert expected == actual

    def test_for_2_mer(self):
        k = 2
        universal_string = k_universal(k)
        assert len(universal_string) == math.pow(2, k)
        expected, actual = self.get_expected_result(universal_string, k)
        assert expected == actual

    def test_for_4_mer(self):
        k = 4
        universal_string = k_universal(k)
        assert len(universal_string) == math.pow(2, k)
        expected, actual = self.get_expected_result(universal_string, k)
        assert expected == actual

    def test_for_5_mer(self):
        k = 5
        universal_string = k_universal(k)
        assert len(universal_string) == int(math.pow(2, k))
        expected, actual = self.get_expected_result(universal_string, k)
        assert expected == actual

    def test_for_6_mer(self):
        k = 6
        universal_string = k_universal(k)
        assert len(universal_string) == int(math.pow(2, k))
        expected, actual = self.get_expected_result(universal_string, k)
        assert expected == actual

    def test_for_7_mer(self):
        k = 7
        universal_string = k_universal(k)
        assert len(universal_string) == int(math.pow(2, k))
        expected, actual = self.get_expected_result(universal_string, k)
        assert expected == actual

    def test_for_10_mer(self):
        k = 10
        universal_string = k_universal(k)
        assert len(universal_string) == int(math.pow(2, k))
        expected, actual = self.get_expected_result(universal_string, k)
        assert expected == actual

if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)
