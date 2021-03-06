import math
from heap_node import HeapNode
from binary_heap import BinaryHeap
from helper.map40 import Map40
import pydot_ng as pydot

class Map(object):
    def __init__(self, intersections, roads):
        self.intersections = intersections
        self.roads = roads

# Class that implements A-star search
class AStar():
    """
    Paramaters:
        map: Reference to map object
        start_node_id: Index of start node
        dest_node_id: Index of destination node
    """
    def __init__(self, map):
        self.map = map
        # Hash set to keep track of open intersections. The hash set will contain intersection IDs only
        # and will be used to find out if an intersection ID is already there is the set
        self.open = set()
        # Hash set to keep track of closed intersection ID. The hash set will contain intersection IDs only
        # and will be used to find out
        self.closed = set()
        # Dictionary to keep track of cost. The dictionary is keyed by intersection id
        # Cost will have three components.
        # g = true of cost of getting from source node to current node
        # h = estimated cost of getting from current node to destination node
        # f = total cost = g + h
        self.cost = {}

        # List used to store the actual path from destination path back to source intersection.
        # Once the shortest path to destination intersection is found, this will be reversed and returned as path from
        # source to destination
        self.nodes_in_path = []
        # Dictionary to keep track of parent intersection. It is keyed by current intersection id.
        # Parent intersection ID is the intersection from where the current intersection is reached
        self.parent = {}
        # Initialize min binary heap. This will be used to get the intersection with minimum cost
        self.cost_heap = BinaryHeap()

    # Private method to get the intersection with minimum total cost
    def _get_node_with_min_cost(self):
        min_value_node = self.cost_heap.delete_min()
        # Remove the intersection with min cost from list of open intersections
        self.open.remove(min_value_node.id)
        # Put that intersection into closed intersections
        self.closed.add(min_value_node.id)
        return min_value_node

    # Returns the list of intersections that can be reached from the current intersection
    def _get_next_nodes(self, current_node_id):
        return self.map.roads[current_node_id]

    # Method that performs A-star search
    def search(self, start_node_id, dest_node_id):
        # Initialize the cost structure of first intersection
        self.cost[start_node_id] = {
            'g': 0, # True cost of getting from start node to this node. This is calculated in terms of number of hops (edges)
            'h': 0, # Estimated cost of getting this node to destination node
            'f': 0  # Total cost. It is a computed field f = g + h
        }
        # Put the start node as the first open node where the search starts
        self.open.add(start_node_id)
        self.cost_heap.insert(HeapNode({'id': start_node_id, 'f': 0, 'g': 0, 'h' : 0}, 'f'))
        iteration = 1
        while len(self.open) > 0:
            # Among all nodes which are open find the node with minimum total cost
            # This will be the nest node to explore
            current_node = self._get_node_with_min_cost()
            if current_node.id == dest_node_id:
                end_node = current_node.id
                while end_node is not None:
                    self.nodes_in_path.append(end_node)
                    end_node = self.parent.get(end_node, None)
                self.nodes_in_path.reverse()
                return self.nodes_in_path
            children = self._get_next_nodes(current_node.id)
            for child in children:
                # If the intersection is already in closed set then there is no need to explore it
                if child in self.closed: continue
                g = self.cost[current_node.id]['g'] + \
                    math.sqrt(
                        math.pow(self.map.intersections[current_node.id][0] - self.map.intersections[child][0], 2) + \
                        math.pow(self.map.intersections[current_node.id][1] - self.map.intersections[child][1], 2))

                # Estimate distance to destination intersection. This is pre euclidean distance.
                # This heuristic will always be less than or equal to the true distance of the road
                # connecting the two intersections
                h = math.sqrt(
                    math.pow(self.map.intersections[child][0] - self.map.intersections[dest_node_id][0], 2) + \
                    math.pow(self.map.intersections[child][1] - self.map.intersections[dest_node_id][1], 2))
                # If the child intersection is not in open set then put it in the list to explore
                # Compute the cost (cost to reach this intersection, estimated cost to reach destination
                # from here and total cost for this intersection
                # The child intersection may already be there if there way another intersection leading to this one
                # Update the cost values if cost of reaching this child intersection is lower than cost value
                # associated with the intersection
                if child not in self.open:
                    self.cost[child] = {'g' : g, 'h' : h, 'f' : g + h}
                    self.parent[child] = current_node.id
                    self.open.add(child)
                    self.cost_heap.insert(HeapNode({'id': child, 'f': g + h, 'g': g, 'h' : h}, 'f'))
                elif self.cost[child]['f'] > g + h:
                    self.cost[child] = {'g' : g, 'h' : h, 'f' : g + h}
                    self.parent[child] = current_node.id
                    self.cost_heap.build_heap()
            #if iteration >= 1:
            #    sys.exit(0)
            iteration += 1

    # Generates SVG diagram for the graph and the shortest path found using A* search
    def draw_astar_map(self, path, colors, output_file):
        graph = pydot.Dot(graph_type='graph', rankdir="LR")
        nodes = {}
        edges = set()

        for k, v in self.map.intersections.items():
            n = pydot.Node(k, shape="circle", style="filled", fillcolor="cyan" if k not in path else colors[0], tooltip="(%f,%f)" % (v[0], v[1]))
            nodes[k] = n
            graph.add_node(n)
        for src, dst in enumerate(self.map.roads):
            for d in dst:
                if (src,d) not in edges:
                    distance = math.sqrt(math.pow(self.map.intersections[src][0] - self.map.intersections[d][0], 2) + \
                                         math.pow(self.map.intersections[src][1] - self.map.intersections[d][1], 2))
                    edges.add((src,d))
                    edges.add((d,src))
                    if src in path and d in path:
                        color = colors[1]
                        style="bold"
                    else:
                        color = "black"
                        style = "dashed"
                    graph.add_edge(pydot.Edge(nodes[src], nodes[d], style=style, label="%0.2f" % distance, color=color, tooltip="%0.2f" % distance))
        graph.write_svg(output_file)

if __name__ == '__main__':
    map_40 = Map(Map40.intersections, Map40.roads)
    astar = AStar(map_40)
    # Assumes the program is executed from current directory
    astar.draw_astar_map(path=astar.search(5, 34), colors=['aquamarine', 'gold'], output_file="../data/map40_5_34.svg")
    astar.draw_astar_map(path=astar.search(8, 24), colors=['deepskyblue', 'gold'], output_file="../data/map40_8_24.svg")

