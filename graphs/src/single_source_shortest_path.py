import math
import sys
from helper.map40 import Map40
import pydot_ng as pydot

# Class implementing graphs
class Graph:
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges

    def get_distance(self, n1 , n2):
        return math.sqrt(math.pow(n1[0] - n2[0], 2) + math.pow(n1[1] - n2[1], 2))

class SingleSourceShortestPath:
    def __init__(self, graph, source):
        # Intialize distance to every node as inifinity except the source node
        self.distance = dict([(index, (index, sys.float_info.max)) if index != source else (index, (source, 0)) for index, n in enumerate(graph.nodes)])
        self.visited = set() # hash set to keep track of already visited nodes
        self.graph = graph
        self.source = source

    def _find_min_distance_node(self):
        min_distance = None
        index = -1
        for i, d in enumerate(self.distance):
            if i in self.visited: continue
            if min_distance is None or min_distance > self.distance[i][1]:
                min_distance = self.distance[i][1]
                index = i
        return index, min_distance


    def find_path(self):
        while len(self.visited) < len(self.graph.nodes):
            min_index, min_distance = self._find_min_distance_node()
            self.visited.add(min_index)
            for n in self.graph.edges[min_index]:
                d = self.graph.get_distance(self.graph.nodes[min_index], self.graph.nodes[n])
                if d + min_distance < self.distance[n][1]:
                    self.distance[n] = (min_index, d + min_distance)
        return self.distance

    def _add_to_edge_list(self, edges, start_node, end_node):
        if start_node in edges:
            edges[start_node].append(end_node)
        else:
            edges[start_node] = [end_node]

    # Orders the nodes in the spanning tree starting from source node.
    # This ordering makes sure that the visualization generated by GraphViz resembles a tree
    def _order_nodes(self, edges):
        ordered_nodes = []
        queue = []
        # Start from source node
        queue.append(self.source)
        visited = set()
        visited.add(self.source)
        while len(queue) > 0:
            node = queue.pop(0)
            if node in visited: continue
            visited.add(node)
            ordered_nodes.append(node)
            queue.extend(edges[node])
        return ordered_nodes

    # From the output of single source shortest path algorithm output generate
    # node and edgelist for spanning tree
    def generate_spanning_tree(self):
        edges = {}
        for k, v in self.find_path().items():
            if k == v[0]: continue
            self._add_to_edge_list(edges, k, v[0])
            self._add_to_edge_list(edges, v[0], k)
        return(self.graph.nodes, [edges[k] for k in sorted(edges.keys())])

    # Generate the SVG diagram of the spanning tree using GraphViz
    def draw_spanning_tree(self, nodes, edges, output_file):
        graph = pydot.Dot(graph_type='graph', rankdir="LR")
        graph_nodes = {}
        graph_edges = set()
        for node in self._order_nodes(edges):
            n = pydot.Node(node, shape="circle", style="filled", fillcolor="cyan", tooltip="(%f,%f)" % (self.graph.nodes[node][0], self.graph.nodes[node][1]))
            graph_nodes[node] = n
            graph.add_node(n)
        for src in self._order_nodes(edges):
            for d in edges[src]:
                if (src,d) not in graph_edges:
                    graph_edges.add((src,d))
                    graph_edges.add((d,src))
                    distance = math.sqrt(math.pow(nodes[src][0] - nodes[d][0], 2) + \
                                         math.pow(nodes[src][1] - nodes[d][1], 2))
                    graph.add_edge(pydot.Edge(graph_nodes[src], graph_nodes[d], label="%0.2f" % distance, tooltip="%0.2f" % distance))
        graph.write_svg(output_file)

if __name__ == '__main__':
    single_source_shortest_path = SingleSourceShortestPath(Graph(Map40.intersections, Map40.roads), 5)
    nodes, edges = single_source_shortest_path.generate_spanning_tree()
    single_source_shortest_path.draw_spanning_tree(nodes, edges, "../data/spanning_tree.svg")