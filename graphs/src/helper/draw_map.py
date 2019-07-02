import pydot_ng as pydot
from helper.map40 import Map40
import math

def draw(road_map, paths, colors):
    graph = pydot.Dot(graph_type='graph', rankdir="LR")
    nodes = {}
    edges = set()

    for k, v in road_map.intersections.items():
        n = pydot.Node(k, shape="circle", style="filled", fillcolor=get_path_id(k, paths, colors), tooltip="(%f,%f)" % (v[0], v[1]))
        nodes[k] = n
        graph.add_node(n)
    for src, dst in enumerate(road_map.roads):
        for d in dst:
            if (src,d) not in edges:
                distance = math.sqrt(math.pow(road_map.intersections[src][0] - road_map.intersections[d][0], 2) + \
                                     math.pow(road_map.intersections[src][1] - road_map.intersections[d][1], 2))
                edges.add((src,d))
                edges.add((d,src))
                found = False
                for index, path in enumerate(paths):
                    if src in path and d in path:
                        graph.add_edge(pydot.Edge(nodes[src], nodes[d], style="bold", label="%0.2f" % distance, color=colors[index], tooltip="%0.2f" % distance))
                        found = True
                if not found:
                    graph.add_edge(pydot.Edge(nodes[src], nodes[d], label="%0.2f" % distance, color="black", tooltip="%0.2f" % distance))
    graph.write_svg("map40.svg")

def get_path_id(node, paths, colors):
    for index, path in enumerate(paths):
        if node in path:
            return colors[index]
    return "cyan"

if __name__ =='__main__':
    draw(Map40, [[5, 16, 37, 12, 34], [8, 14, 16, 37, 12, 17, 10, 24]], ['aquamarine', 'deepskyblue', 'gold'])
