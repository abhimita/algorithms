#python3
import sys
import collections
import re
import unittest

def build_graph(graph):
    in_degree = collections.defaultdict(int)
    out_degree = collections.defaultdict(int)
    adj_list = collections.defaultdict(list)
    vertices_lookup = collections.defaultdict(int)
    vertices_reverse_lookup = collections.defaultdict(int)
    non_one_to_one_nodes = set()
    node_num = 0
    for line in graph:
        entry = re.split('\s+->\s+', line)
        source = int(entry[0])
        destinations = entry[1]
        if source not in vertices_lookup.keys():
            vertices_lookup[source] = node_num
            vertices_reverse_lookup[node_num] = source
            node_num += 1
        s = vertices_lookup[source]
        for destination in map(int, destinations.split(',')):
            if destination not in vertices_lookup.keys():
                vertices_lookup[destination] = node_num
                vertices_reverse_lookup[node_num] = int(destination)
                node_num += 1
            d = vertices_lookup[destination]
            adj_list[int(s)].append(int(d))
            in_degree[d] += 1
            out_degree[s] += 1
    for v in vertices_reverse_lookup.keys():
        if in_degree[v] == 1 and out_degree[v] == 1:
            continue
        non_one_to_one_nodes.add(v)
    return adj_list, node_num, vertices_reverse_lookup, in_degree, out_degree, non_one_to_one_nodes

def find_paths(graph):
    adj_list, n, vertices_reverse_lookup, in_degree, out_degree, non_one_to_one_nodes = build_graph(graph)
    paths = []
    for v in non_one_to_one_nodes:
        if out_degree[v] > 0:
            while len(adj_list[v]) > 0:
                nbr = adj_list[v].pop(0)
                p = [vertices_reverse_lookup[v]]
                w = nbr
                while in_degree[w] == 1 and out_degree[w] == 1:
                    p.append(vertices_reverse_lookup[w])
                    w = adj_list[w].pop(0)
                p.append(vertices_reverse_lookup[w])
                paths.append('->'.join(map(str, p)))
    return '\n'.join(paths + detect_isolated_cylces(adj_list, vertices_reverse_lookup))

def detect_isolated_cylces(adj_list, vertices_reverse_lookup):
    cycles = []
    for v in adj_list.keys():
        c = []
        if len(adj_list[v]) == 0: continue
        c.append(vertices_reverse_lookup[v])
        w = v
        while len(adj_list[w]) > 0:
            w = adj_list[w].pop(0)
            c.append(vertices_reverse_lookup[w])
        cycles.append('->'.join(map(str, c)))
    return cycles

def dfs_cycle(adj_list, n):
    parent = [-1] * n
    cycle = [0] * n
    visited = [False] * n
    in_stack = [False] * n
    cycle_number = 0

    def dfs_cycle_recursive(start_node, parent_node=None):
        nonlocal cycle_number
        if visited[start_node]: return
        if in_stack[start_node]:
            cycle_number += 1
            cycle[start_node] = cycle_number
            p = parent_node
            while p != start_node:
                cycle[p] = cycle_number
                p = parent[p]
            return
        in_stack[start_node] = True
        for nbr in adj_list[start_node]:
            parent[nbr] = start_node
            dfs_cycle_recursive(nbr, start_node)
        visited[start_node] = True
        in_stack[start_node] = False
    i = 0
    while i < len(parent):
        if parent[i] == -1:
            print(i, parent)
            parent[i] = i
            dfs_cycle_recursive(i, parent[i])
        i += 1
    return cycle, parent

class TestMaxNonBranchingPath(unittest.TestCase):

    def test_for_two_disjoint_components(self):
        graph = [
            '1 -> 2',
            '2 -> 3',
            '3 -> 4,5',
            '6 -> 7',
            '7 -> 6'
        ]
        actual = find_paths(graph)
        expected = '\n'.join(['1->2->3', '3->4', '3->5', '6->7->6'])
        assert actual == expected

    def test_max_non_braching_path_doesnot_have_1_on_1_nodes_other_than_start_end(self):
        graph = [
            '0 -> 1',
            '1 -> 2',
            '2 -> 3,4'
        ]
        actual = find_paths(graph)
        expected = '\n'.join(['0->1->2', '2->3', '2->4'])
        assert actual == expected

    def test_two_disjoint_component_and_cycle(self):
        graph = [
            '5 -> 3',
            '3 -> 4',
            '1 -> 2',
            '6 -> 1',
            '2 -> 6'
        ]

        actual = find_paths(graph)
        expected = '\n'.join(['5->3->4', '1->2->6->1'])
        assert actual == expected

    def test_for_many_short_non_branching_path(self):
        graph = [
            '1 -> 2',
            '2 -> 3,4,5',
            '4 -> 6,10',
            '5 -> 7',
            '6 -> 10'
        ]
        actual = find_paths(graph)
        expected = '\n'.join(['1->2', '2->3', '2->4', '2->5->7', '4->6->10', '4->10'])
        assert actual == expected

    def test_for_long_branching_path(self):
        graph = [
            '7 -> 10',
            '10 -> 14',
            '14 -> 3,5,18',
            '5 -> 4',
            '52 -> 13',
            '4 -> 8',
            '8 -> 14',
            '18 -> 19',
            '19 -> 31',
            '31 -> 52'
        ]
        actual = find_paths(graph)
        expected = '\n'.join(['7->10->14', '14->3', '14->5->4->8->14', '14->18->19->31->52->13'])
        assert actual == expected

    def test_for_isolated_cycles(self):
        graph = [
            '7 -> 3',
            '3 -> 4',
            '4 -> 8',
            '8 -> 9',
            '9 -> 7',
            '1 -> 2',
            '2 -> 5',
            '5 -> 10',
            '10 -> 2',
            '16 -> 111',
            '111 -> 16'
        ]
        actual = find_paths(graph)
        expected = '\n'.join(['1->2', '2->5->10->2', '7->3->4->8->9->7', '16->111->16'])
        assert actual == expected

if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)

