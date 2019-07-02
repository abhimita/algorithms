import pydot_ng as pydot
from helper.map40 import Map40
import math

def draw(road_map, path, colors, output_file):
    graph = pydot.Dot(graph_type='graph', rankdir="LR")
    nodes = {}
    edges = set()

    for k, v in road_map.intersections.items():
        n = pydot.Node(k, shape="circle", style="filled", fillcolor="cyan" if k not in path else colors[0], tooltip="(%f,%f)" % (v[0], v[1]))
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
                if src in path and d in path:
                    color = colors[1]
                    style="bold"
                else:
                    color = "black"
                    style = "dashed"
                graph.add_edge(pydot.Edge(nodes[src], nodes[d], style=style, label="%0.2f" % distance, color=color, tooltip="%0.2f" % distance))
    graph.write_svg(output_file)

if __name__ =='__main__':
    draw(road_map=Map40, path=[5, 16, 37, 12, 34], colors=['aquamarine', 'gold'], output_file="map40_5_34.svg")
    draw(road_map=Map40, path=[8, 14, 16, 37, 12, 17, 10, 24], colors=['deepskyblue', 'gold'], output_file="map40_8_24.svg")
