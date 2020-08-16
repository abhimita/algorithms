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
    return adj_list, vertices, in_degree, out_degree

def eulerian_cycle(graph, start_node=None):
    adj_list, vertices, in_degree, out_degree = convert_to_graph(graph)
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

    for v in vertices:
        if in_degree[v] != out_degree[v]:
            raise Exception('Graph can not have Eulerian cycle (node %s)' % v)
    vertex_list = list(vertices)
    traverse(vertex_list[0] if start_node is None else start_node)
    vertices_in_path.reverse()
    return '->'.join(vertices_in_path)

class TestEulerianCycle(unittest.TestCase):
    def get_edge_list_from_graph(self, graph):
        edges = collections.defaultdict(int)
        for r in graph:
            src, dest = re.split('\s+->\s+', r)
            for d in dest.split(','):
                edges[(src, d)] = 0
        return edges

    def check_euler_cycle(self, euler_cycle, edges):
        nodes = re.split('->', euler_cycle)
        # Check that first and  last node is same
        if nodes[0] != nodes[len(nodes) - 1]:
            return False
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
        graph = ['0 -> 3', '1 -> 0', '2 -> 1,6', '3 -> 2', '4 -> 2', '5 -> 4', '6 -> 5,8', '7 -> 9', '8 -> 7', '9 -> 6']
        actual = eulerian_cycle(graph, '3')
        assert(self.check_euler_cycle(actual, self.get_edge_list_from_graph(graph)) == True)

    def test_for_small_graph(self):
        graph = ['0 -> 1', '1 -> 2', '2 -> 0']
        actual = eulerian_cycle(graph, '0')
        assert(self.check_euler_cycle(actual, self.get_edge_list_from_graph(graph)) == True)

    def test_for_start_node_with_multiple_outgoing_edges(self):
        graph = ['0 -> 3,1', '1 -> 2', '2 -> 0', '3 -> 0']
        actual = eulerian_cycle(graph, '0')
        assert(self.check_euler_cycle(actual, self.get_edge_list_from_graph(graph)) == True)

    def test_for_eulerian_cycle_not_starting_at_node_zero(self):
        graph = ['0 -> 1', '1 -> 2,3', '2 -> 0',  '3 -> 4', '4 -> 1']
        actual = eulerian_cycle(graph, '4')
        assert(self.check_euler_cycle(actual, self.get_edge_list_from_graph(graph)) == True)

    def test_for_self_loop(self):
        graph = ['1 -> 2', '2 -> 1,2']
        actual = eulerian_cycle(graph, '2')
        assert(self.check_euler_cycle(actual, self.get_edge_list_from_graph(graph)) == True)

    def test_for_two_digit_node_number(self):
        graph = ['1 -> 10', '10 -> 2,3,4', '2 -> 1', '3 -> 10', '4 -> 5', '5 -> 10']
        actual = eulerian_cycle(graph, '1')
        assert(self.check_euler_cycle(actual, self.get_edge_list_from_graph(graph)) == True)

    def test_for_highly_connected_graph(self):
        graph = ['0 -> 1,2,3,4', '1 -> 0,2,3,4', '2 -> 0,1,3,4', '3 -> 0,1,2,4', '4 -> 0,1,2,3']
        actual = eulerian_cycle(graph, '3')
        assert(self.check_euler_cycle(actual, self.get_edge_list_from_graph(graph)) == True)

if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)