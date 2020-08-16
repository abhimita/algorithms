#python3
import sys
import collections
import unittest

def de_bruijn(patterns):

    in_degree = collections.defaultdict(int)
    out_degree = collections.defaultdict(int)
    adj_list = collections.defaultdict(list)
    vertices = set()
    non_one_to_one_nodes = set()

    for p in patterns:
        src = p[:-1]
        dst = p[1:]
        adj_list[src].append(dst)
        in_degree[dst] += 1
        out_degree[src] += 1
        vertices.add(src)
        vertices.add(dst)
    for v in vertices:
        if in_degree[v] == 1 and out_degree[v] == 1: continue
        non_one_to_one_nodes.add(v)
    return adj_list, in_degree, out_degree, non_one_to_one_nodes

def detect_isolated_cycles(adj_list):
    cycles = []
    for v in adj_list.keys():
        c = []
        if len(adj_list[v]) == 0: continue
        c.append(v)
        w = v
        while len(adj_list[w]) > 0:
            w = adj_list[w].pop(0)
            c.append(w)
        cycles.append(''.join([x if i == 0 else x[-1] for i,x in enumerate(c)]))
    return cycles

def contigs(patterns):
    adj_list, in_degree, out_degree, non_one_to_one_nodes = de_bruijn(patterns)
    paths = []
    for v in non_one_to_one_nodes:
        if out_degree[v] > 0:
            while len(adj_list[v]) > 0:
                nbr = adj_list[v].pop(0)
                p = [v]
                w = nbr
                while in_degree[w] == 1 and out_degree[w] == 1:
                    p.append(w)
                    w = adj_list[w].pop(0)
                p.append(w)
                paths.append(''.join([x if i == 0 else x[-1] for i,x in enumerate(p)]))
    return ' '.join(paths + detect_isolated_cycles(adj_list))

class TestContigs(unittest.TestCase):
    def test_first_sample_dataset(self):
        patterns = [
            'ATG', 'ATG', 'TGT', 'TGG', 'CAT', 'GGA', 'GAT', 'AGA'
        ]
        actual = contigs(patterns)
        expected = ['GAT', 'CAT', 'AGA', 'TGT', 'TGGA', 'ATG', 'ATG']
        assert ' '.join(sorted(actual.split(' '))) == ' '.join(sorted(expected))

    def test_general_approach(self):
        patterns = [
            'AG', 'GT', 'GC', 'TA'
        ]
        actual = contigs(patterns)
        expected = ['GTAG', 'GC']
        assert ' '.join(sorted(actual.split(' '))) == ' '.join(sorted(expected))

    def test_self_loop(self):
        patterns = [
            'GTT', 'TTA', 'TAC', 'TTT'
        ]
        actual = contigs(patterns)
        expected = ['GTT', 'TTAC', 'TTT']
        assert ' '.join(sorted(actual.split(' '))) == ' '.join(sorted(expected))

    def test_repeated_kmers(self):
        patterns = [
            'TGAG', 'GACT', 'CTGA', 'ACTG', 'CTGA'
        ]
        actual = contigs(patterns)
        expected = ['TGAG', 'GACTG', 'CTGA', 'CTGA']
        assert ' '.join(sorted(actual.split(' '))) == ' '.join(sorted(expected))

    def test_isolated_cycles(self):
        patterns = [
            'GAGA', 'AGAG', 'AACG', 'ACGT', 'ACGG'
        ]
        actual = contigs(patterns)
        expected = ['AACG', 'ACGT', 'ACGG', 'GAGAG']
        assert ' '.join(sorted(actual.split(' '))) == ' '.join(sorted(expected))

if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)