import re
from collections import defaultdict
import unittest

def build_graph(edges):
    predecessor = defaultdict(list)
    vertices = set()
    for e in edges:
        src, dest_cost = re.split(r'\s*->\s*', e)
        dest, cost = map(int, dest_cost.split(':'))
        src = int(src)
        predecessor[dest].append({'source': src, 'cost' : cost})
        vertices.add(src)
        vertices.add(dest)
    return predecessor, vertices

def longest_path(source, sink, edges):
    predecessor, vertices = build_graph(edges)
    cost = defaultdict(lambda: float('-inf'))
    cost[source] = 0
    parent = [-1] * (max(list(vertices)) + 1)
    for s in sorted(predecessor.keys()):
        if s <= source: continue
        for p in predecessor[s]:
            if cost[p['source']] + p['cost'] > cost[s]:
                parent[s] = p['source']
                cost[s] =  cost[p['source']] + p['cost']
    s = sink
    path = []
    while s >= source:
        path.append(s)
        s = parent[s]
    return cost[sink], '->'.join(map(str, reversed(path)))

class LongestPathDAG(unittest.TestCase):
    def test_base_case(self):
        source = 0
        sink = 4
        edges = ["0->1:7", "0->2:4", "2->3:2", "1->4:1", "3->4:3"]
        cost, path = longest_path(source,sink,edges)
        assert cost == 9
        assert path == '0->2->3->4'

    def test_output_is_longest_path_not_shortest_path(self):
        source = 0
        sink = 3
        edges = ["0->1:1", "0->3:10", "1->2:1", "2->3:1"]
        cost, path = longest_path(source,sink,edges)
        assert cost == 10
        assert path == '0->3'

    def test_parsing_correctness(self):
        source = 0
        sink = 3
        edges = ["0->1:2", "0->2:1", "1->3:3", "2->3:3"]
        cost, path = longest_path(source,sink,edges)
        assert cost == 5
        assert path == '0->1->3'

    def test_greedy_strategy_is_not_used(self):
        source = 0
        sink = 3
        edges = ["0->1:1", "0->2:5", "1->3:10", "2->3:1"]
        cost, path = longest_path(source,sink,edges)
        assert cost == 11
        assert path == '0->1->3'

    def test_code_does_not_rely_on_source_node_not_being_zero(self):
        source = 1
        sink = 4
        edges = ["1->2:1", "1->3:5", "2->4:10", "3->4:1"]
        cost, path = longest_path(source,sink,edges)
        assert cost == 11
        assert path == '1->2->4'

    def test_parsing_can_handle_double_digit_node_label(self):
        source = 1
        sink = 10
        edges = ["1->2:1", "2->3:3", "3->10:1"]
        cost, path = longest_path(source,sink,edges)
        assert cost == 5
        assert path == '1->2->3->10'

    def test_for_graph_with_one_edge_only(self):
        source = 0
        sink = 4
        edges = ["0->4:7"]
        cost, path = longest_path(source,sink,edges)
        assert cost == 7
        assert path == '0->4'

    def test_when_cost_negative(self):
        source = 1
        sink = 5
        edges = ["0->1:5", "0->2:3", "1->3:6", "1->2:2", "3->4:-1", "3->5:1", "2->3:7", "2->4:4", "2->5:2", "4->5:-2"]
        cost, path = longest_path(source,sink,edges)
        assert cost == 10
        assert path == '1->2->3->5'


unittest.main(argv=[''], verbosity=2, exit=False)