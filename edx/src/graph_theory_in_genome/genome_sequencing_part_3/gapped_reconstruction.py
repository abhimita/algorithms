import sys
import unittest
from collections import defaultdict
from functools import reduce
import itertools
import copy

def validate_path(eulerian_path, k, d):
    merged_list = reduce(lambda x,y: x + y, ([p if i == 0 else list(map(lambda x: x[-1], p)) for i, p in enumerate([e.split('|') for e in eulerian_path])]))
    first_string = second_string = ''
    for m in range(0, len(merged_list), 2):
        first_string = first_string + merged_list[m]
        second_string = second_string + merged_list[m + 1]
    if first_string[k + d:] != second_string[:len(first_string[k + d:])]:
        return -1, None
    return 0, first_string[: (k + d)] + second_string

def convert_to_graph(k, paired_comp):
    adj_list = defaultdict(list)
    vertices = set()
    in_degree = defaultdict(int)
    out_degree = defaultdict(int)
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
    return adj_list, vertices, in_degree, out_degree, start_node

def reconstruct(k, d, paired_comp):
    adj_list_copy, vertices, in_degree, out_degree, start_node = convert_to_graph(k, paired_comp)
    branching_nodes = [k for k in adj_list_copy.keys() if len(adj_list_copy[k]) > 1]
    branching_options = list(itertools.product(*[adj_list_copy[b] for b in branching_nodes]))

    def traverse(start_node):
        while len(adj_list[start_node]) > 0:
            nbr = adj_list[start_node].pop(0)
            traverse(nbr)
        vertices_in_path.append(start_node)
        return vertices_in_path

    vertex_list = list(vertices)
    while True:
        vertices_in_path = []
        adj_list = copy.deepcopy(adj_list_copy)
        if len(branching_options) > 0:
            first_elements = branching_options.pop(0)
            for i, n in enumerate(branching_nodes):
                if first_elements[i] == adj_list[n][0]: continue
                index = adj_list[n].index(first_elements[i])
                adj_list[n][0], adj_list[n][index] = adj_list[n][index], adj_list[n][0]
        traverse(vertex_list.pop(0) if start_node is None else start_node)
        vertices_in_path.reverse()
        can_be_merged, merged_string = validate_path(vertices_in_path, k, d)
        if can_be_merged != -1:
            break
    return merged_string


class TestPairedReadReconstruction(unittest.TestCase):
    def test_base_case(self):
        k = 4
        d = 2
        paired_comp = ['ACAC|CTCT', 'ACAT|CTCA', 'CACA|TCTC', 'GACA|TCTC']
        assert reconstruct(k, d, paired_comp) == 'GACACATCTCTCA'

    def test_random_order(self):
        k = 3
        d = 1
        paired_comp = ['TCA|GCA', 'TTC|TGC', 'AAT|CAT', 'ATT|ATG']
        assert reconstruct(k, d, paired_comp) == 'AATTCATGCA'

    def test_multiple_euler_paths(self):
        k = 2
        d = 1
        paired_comp = ['GG|GA', 'GT|AT', 'TG|TA', 'GA|AC', 'AT|CT']
        assert reconstruct(k, d, paired_comp) == 'GGTGATACT'

    def test_multiple_repeater_kmers(self):
        k = 3
        d = 2
        paired_comp = ['GGG|GGG', 'AGG|GGG', 'GGG|GGT', 'GGG|GGG', 'GGG|GGG']
        assert reconstruct(k, d, paired_comp) == 'AGGGGGGGGGGT'

    def test_euler_cycle(self):
        k = 4
        d = 2
        paired_comp = ['GTTT|ATTT', 'TTTA|TTTG', 'TTAC|TTGT', 'TACG|TGTA', 'ACGT|GTAT', 'CGTT|TATT']
        actual = reconstruct(k, d, paired_comp)
        assert actual == 'TTTACGTTTGTATTT'

if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)
