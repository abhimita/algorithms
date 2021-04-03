#python3
import sys
import re
import collections
import unittest

# Find a longest path between two nodes in an edge-weighted DAG.
# Input: An edge-weighted graph, a source node source, and a sink node sink.
# Output: The length of the longest path from source to sink, followed by a longest path.

# A Directed Acyclic Graph (DAG) is a graph that does not contain any directed cycles. The length of a
# path in an edge-weighted graph is given by the sum of its edge weights. Given nodes source and sink,
# our goal is to find a longest path from source to sink. We assume that all nodes of the graph have
# integer labels and ordering the nodes in ascending represents a topological order,
# i.e., all edges of the graph connect a node with smaller label to a node with a larger label.

# Input Format. The first line of the input contains an integer representing source that has the
# smallest label. The second line of the input contains an integer representing sink that has the
# largest label. Each of the remaining lines represents an edge in the graph G(V,E) with node-set V and
# edge-set E, where each line is in the format u->v:w denoting an edge from node u to node v with weight w.

# Output Format. The first line of the output should contain a number representing the length of the
# longest path from source to sink. The second line of the output should be a longest path in the format
# source->a->b->c->...->sink, where each of the items delimited by -> is a node in G. (If multiple longest
# paths exist, you may return any one.)

def build_graph(edges):
    adj_list = collections.defaultdict(list)
    vertices = set()
    for e in edges:
        src, dest_cost = re.split(r"\s*->\s*", e)
        dest, cost = dest_cost.split(':')
        adj_list[int(src)].append({'dest': int(dest), 'cost': int(cost)})
        vertices.add(int(src))
        vertices.add(int(dest))
    return adj_list, vertices

def topological_sort(adj_list, vertices, source, sink):
    sorted_nodes = []
    visited = [False] * (max(vertices) + 1)
    def traverse(source):
        visited[source] = True
        for nbr in adj_list[source]:
            if not visited[nbr['dest']]:
                traverse(nbr['dest'])
        sorted_nodes.append(source)
    traverse(source)
    return sorted_nodes

def longest_path(source, sink, edges):
    adj_list, vertices = build_graph(edges)
    sorted_nodes = topological_sort(adj_list, vertices, source, sink)
    print(list(reversed(sorted_nodes)))
    print(adj_list)
    cost = [float('-inf')] * (max(vertices) + 1)
    cost[source] = 0
    longest_path = [-1] * (max(vertices) + 1)
    for i in range(len(sorted_nodes) - 1, -1, -1):
        for nbr in adj_list[sorted_nodes[i]]:
            if cost[sorted_nodes[i]] + nbr['cost'] > cost[nbr['dest']]:
                cost[nbr['dest']] = cost[sorted_nodes[i]] + nbr['cost']
                longest_path[nbr['dest']] = sorted_nodes[i]
    s = sink
    path = []
    while True:
        path.append(s)
        if s == source: break
        s = longest_path[s]
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

    def test_code_does_not_rely_on_source_node_being_zero(self):
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
        print(path)

    def test_when_graph_has_multiple_sinks(self):
        source = 7
        sink = 2
        edges = ["0->6:2", "1->6:8", "1->4:1", "1->2:-4", "3->4:5", "3->0:3", "5->1:2", "7->3:4", "7->0:6", "7->1:-1", "7->5:-4"]
        cost, path = longest_path(source,sink,edges)
        print(cost)
        print(path)

    def test_foo(self):
        source = 0
        sink = 3
        edges = ["0->1:-2", "0->5:5", "5->1:-8", "1->3:12", "5->3:4", "0->3:11"]
        cost, path = longest_path(source,sink,edges)
        print(cost)
        print(path)

unittest.main(argv=[''], verbosity=2, exit=False)