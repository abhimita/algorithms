#python3
import sys
import collections
import re
import unittest

def convert_to_graph(graph):
    vertices = set()
    adj_list = collections.defaultdict(list)
    in_degree = collections.defaultdict(int)
    out_degree = collections.defaultdict(int)
    for r in graph:
        e = re.split('\s+->\s+', r)
        out_degree[e[0]] += len(e[1].split(','))
        vertices.add(e[0])
        for d in e[1].split(','):
            vertices.add(d)
            adj_list[e[0]].append(d)
            in_degree[d] += 1
    start_node = end_node = None
    for v in vertices:
        if out_degree[v] - in_degree[v] == 1:
            start_node = v
        elif in_degree[v] - out_degree[v] == 1:
            end_node = v
    return adj_list, vertices, in_degree, out_degree, start_node, end_node

def eulerian_path(graph):
    adj_list, vertices, in_degree, out_degree, start_node, end_node = convert_to_graph(graph)
    vertices_in_path = []
    edges_visited = set()
    def traverse(start_node):
        for nbr in adj_list[start_node]:
            edge = '%s->%s' % (start_node, nbr)
            if edge in edges_visited:
                continue
            edges_visited.add(edge)
            traverse(nbr)
        vertices_in_path.append(start_node)
        return vertices_in_path

    vertex_list = list(vertices)
    traverse(vertex_list[0] if start_node is None else start_node)
    vertices_in_path.reverse()
    return '->'.join(vertices_in_path)

class TestEulerianPath(unittest.TestCase):
    def convert_graph_to_edge_list(self, graph):
        edges = collections.defaultdict(int)
        for r in graph:
            src, dest = re.split('\s+->\s+', r)
            for d in dest.split(','):
                edges[(src, d)] = 0
        return edges

    def check_euler_path(self, euler_cycle, edges):
        nodes = re.split('->', euler_cycle)
        # Check if every edge has been visited once only
        for i in range(len(nodes) - 1):
            src = nodes[i]
            dest = nodes[i + 1]
            edges[(src,dest)] += 1
        for k in edges.keys():
            if edges[k] != 1:
                return False
        return True

    def test_for_ten_node_graph(self):
        graph = ['0 -> 2', '1 -> 3', '2 -> 1', '3 -> 0,4', '6 -> 3,7', '7 -> 8', '8 -> 9', '9 -> 6']
        actual = eulerian_path(graph)
        assert(self.check_euler_path(actual, self.convert_graph_to_edge_list(graph)) == True)

    def test_graph_with_two_nodes_with_unbalanced_in_out_degree(self):
        graph = ['0 -> 1', '1 -> 2', '2 -> 3']
        actual = eulerian_path(graph)
        assert(self.check_euler_path(actual, self.convert_graph_to_edge_list(graph)) == True)

    def test_graph_with_simple_loop(self):
        graph = ['0 -> 1', '1 -> 2,5', '2 -> 3', '3 -> 4', '4 -> 1']
        actual = eulerian_path(graph)
        assert(self.check_euler_path(actual, self.convert_graph_to_edge_list(graph)) == True)

    def test_graph_with_source_node_having_higher_label(self):
        graph = ['2 -> 1', '1 -> 3,4,0', '3 -> 1,4', '4 -> 3,1']
        actual = eulerian_path(graph)
        assert(self.check_euler_path(actual, self.convert_graph_to_edge_list(graph)) == True)

    def test_graph_with_double_digit_nodes(self):
        graph = ['0 -> 1', '1 -> 14,17', '14 -> 2,3,4', '2 -> 1', '3 -> 14', '4 -> 5', '5 -> 14']
        actual = eulerian_path(graph)
        assert(self.check_euler_path(actual, self.convert_graph_to_edge_list(graph)) == True)

    def test_graph_with_high_in_out_degree_for_src_sink(self):
        graph = ['2 -> 3,5', '3 -> 4', '4 -> 2', '5 -> 6', '6 -> 2', '1 -> 2,0', '0 -> 1']
        actual = eulerian_path(graph)
        assert(self.check_euler_path(actual, self.convert_graph_to_edge_list(graph)) == True)

if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)