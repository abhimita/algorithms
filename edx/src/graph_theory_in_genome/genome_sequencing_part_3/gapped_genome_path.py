import sys
import collections
from functools import reduce
import unittest

def reconstruct(k, d, paired_comp):
    adj_list = collections.defaultdict(list)
    vertices = set()
    in_degree = collections.defaultdict(int)
    out_degree = collections.defaultdict(int)
    for p in paired_comp:
        paired_kmers = p.split('|')
        src_node = '%s|%s' % (paired_kmers[0][:k - 1], paired_kmers[1][:k - 1])
        dest_node = '%s|%s' % (paired_kmers[0][1:], paired_kmers[1][1:])
        vertices.add(src_node)
        vertices.add(dest_node)
        out_degree[src_node] += 1
        in_degree[dest_node] += 1
        adj_list[src_node].append(dest_node)
    start_node = None
    for v in vertices:
        if out_degree[v] == in_degree[v] + 1:
            start_node = v
            break
    eulerian_path = []
    if start_node is None:
        start_node = list(vertices)[0]

    def traverse(start_node):
        while len(adj_list[start_node]) > 0:
            nbr = adj_list[start_node].pop(0)
            traverse(nbr)
        eulerian_path.append(start_node)

    if start_node is None:
        for v in list(vertices):
            start_node = v
            traverse(start_node)
            eulerian_path.reverse()
            can_be_merged, merged_string = validate_path(eulerian_path, k, d)
            if can_be_merged == -1:
                eulerian_path = []
            else:
                break
    else:
        traverse(start_node)
        eulerian_path.reverse()
        can_be_merged, merged_string = validate_path(eulerian_path, k, d)
    return merged_string


def validate_path(eulerian_path, k, d):
    merged_list = reduce(lambda x,y: x + y, ([p if i == 0 else list(map(lambda x: x[-1], p)) for i, p in enumerate([e.split('|') for e in eulerian_path])]))
    first_string = second_string = ''
    for m in range(0, len(merged_list), 2):
        first_string = first_string + merged_list[m]
        second_string = second_string + merged_list[m + 1]
    if first_string[k + d:] != second_string[:len(first_string[k + d:])]:
        return -1, None
    return 0, first_string[: (k + d)] + second_string

class TestPairedDeBruijnGraph(unittest.TestCase):
    def test_for_k_4_and_d_2(self):
        k = 4
        d = 2
        paired_comp = ['ACAC|CTCT', 'ACAT|CTCA', 'CACA|TCTC', 'GACA|TCTC']
        actual = reconstruct(k, d, paired_comp)
        expected = 'GACACATCTCTCA'
        assert actual == expected

    def test_when_k_is_greater_than_d(self):
        k = 5
        d = 1
        paired_comp = ['ACAGC|GCGAA', 'CAGCT|CGAAT', 'AGCTG|GAATC', 'GCTGC|AATCA']
        actual = reconstruct(k, d, paired_comp)
        assert actual == 'ACAGCTGCGAATCA'

    def test_when_k_is_less_than_d(self):
        k = 2
        d = 4
        paired_comp = ['GC|CG', 'CA|GT', 'AT|TG', 'TA|GC', 'AC|CA', 'CC|AT']
        actual = reconstruct(k, d, paired_comp)
        assert actual == 'GCATACCGTGCAT'

    def test_basic_case(self):
        k = 2
        d = 1
        paired_comp = ['AC|TT', 'CG|TG', 'GT|GA', 'TT|AC']
        actual = reconstruct(k, d, paired_comp)
        assert actual == 'ACGTTGAC'

    # def test_pairs_with_no_apparent_order(self):
    #     k = 3
    #     d = 1
    #     paired_comp = ['TCA|GCA', 'TTC|TGC', 'AAT|CAT', 'ATT|ATG']
    #     actual = reconstruct(k, d, paired_comp)
    #     expected = 'AATTCATGCA'
    #     assert actual == expected
    #
    # def test_two_alternate_eulerian_path(self):
    #     k = 2
    #     d = 1
    #     paired_comp = ['GG|GA', 'GT|AT', 'TG|TA', 'GA|AC', 'AT|CT']
    #     actual = reconstruct(k, d, paired_comp)
    #     print(actual)

    # def test_with_no_specific_starting_point(self):
    #     k = 4
    #     d = 2
    #     paired_comp = ['GTTT|ATTT', 'TTTA|TTTG', 'TTAC|TTGT', 'TACG|TGTA', 'ACGT|GTAT', 'CGTT|TATT']
    #     actual = reconstruct(k, d, paired_comp)
    #     print(actual)

if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)