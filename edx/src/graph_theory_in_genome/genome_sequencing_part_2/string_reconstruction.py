import collections
import unittest
import sys

def reconstruct(k, patterns):
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
    start_node = None
    for v in vertices:
        if out_degree[v] == in_degree[v] + 1:
            start_node = v
    if start_node is None:
        start_node = list(vertices)[0]
    vertices_in_path = []
    def traverse(start_node):
        while len(adj_list[start_node]) > 0:
            nbr = adj_list[start_node].pop(0)
            traverse(nbr)
        vertices_in_path.append(start_node)
        return vertices_in_path
    vertices_in_path = traverse(start_node)
    vertices_in_path.reverse()
    return ''.join([v if i == 0 else v[-1] for i, v in enumerate(vertices_in_path)])

class TestReconstruct(unittest.TestCase):
    def test_for_basic_kmers(self):
        k_mers = ['ACG', 'CGT', 'GTG', 'TGT', 'GTA', 'TAT', 'ATA']
        actual = reconstruct(3, k_mers)
        assert actual == 'ACGTGTATA'

    def test_for_when_kmers_donot_appear_in_seq(self):
        k_mers = ['GG', 'AC', 'GA', 'CT']
        actual = reconstruct(2, k_mers)
        assert actual == 'GGACT'

    def test_for_repeating_kmers(self):
        k_mers = ['AAC', 'AAC', 'ACG', 'ACT', 'CGA', 'GAA']
        actual = reconstruct(3, k_mers)
        assert actual == 'AACGAACT'

    def test_for_multiple_eulerian_paths(self):
        k_mers = ['CTAC', 'CTCC', 'TCCT', 'ACTC', 'CCTC', 'CCTA', 'TACT']
        actual = reconstruct(4, k_mers)
        assert actual == 'CCTCCTACTC' or actual == 'CCTACTCCTC'

    def test_for_many_duplicate_kmers(self):
        k_mers = ['CCC', 'CCC', 'CCC', 'TCC', 'CCC', 'CCG', 'CCC', 'CCC', 'CCC']
        actual = reconstruct(3, k_mers)
        assert actual == 'TCCCCCCCCCG'

    def test_for_source_and_sink_duplicate_kmer(self):
        k_mers = ['AG', 'AT', 'AA', 'GA', 'GG', 'GT', 'TA', 'TG', 'TT', 'AT']
        actual = reconstruct(2, k_mers)
        assert actual == 'AAGTTGGATAT' or actual == 'AGATAATGGTT'

    def test_for_eulerian_cycle_in_debruijn_graph(self):
        k_mers = ['ACG', 'CGT', 'GTA', 'TAC']
        actual = reconstruct(3, k_mers)
        assert actual == 'ACGTAC'

if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)

