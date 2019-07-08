import unittest
from helper.map40 import Map40
from single_source_shortest_path import SingleSourceShortestPath, Graph

class TestAStar(unittest.TestCase):
    def test_map_with_40_nodes_start_5_end_34(self):
        start_node_id = 5
        dest_node_id = 34
        paths = SingleSourceShortestPath(Graph(Map40.intersections, Map40.roads), start_node_id).find_path()
        shortest_path = []
        while paths[dest_node_id][1] != 0:
            shortest_path.append(dest_node_id)
            dest_node_id = paths[dest_node_id][0]
        shortest_path.append(dest_node_id)
        shortest_path.reverse()
        self.assertEqual(shortest_path, [5, 16, 37, 12, 34])

    def test_map_with_40_nodes_start_8_end_24(self):
        start_node_id = 8
        dest_node_id = 24
        paths = SingleSourceShortestPath(Graph(Map40.intersections, Map40.roads), start_node_id).find_path()
        shortest_path = []
        while paths[dest_node_id][1] != 0:
            shortest_path.append(dest_node_id)
            dest_node_id = paths[dest_node_id][0]
        shortest_path.append(dest_node_id)
        shortest_path.reverse()
        self.assertEqual(shortest_path, [8, 14, 16, 37, 12, 17, 10, 24])

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SingleSourceShortestPath)
    unittest.TextTestRunner(verbosity=2).run(suite)