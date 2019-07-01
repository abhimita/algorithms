import unittest
from helper.map40 import Map40
from astar import Map, AStar

class TestAStar(unittest.TestCase):
    def test_map_with_40_nodes_start_5_end_34(self):
        map_40 = Map(Map40.intersections, Map40.roads)
        start_node_id = 5
        dest_node_id = 34
        astar = AStar(map_40, start_node_id, dest_node_id)
        self.assertEqual(astar.search(), [5, 16, 37, 12, 34])

    def test_map_with_40_nodes_start_5_end_24(self):
        map_40 = Map(Map40.intersections, Map40.roads)
        start_node_id = 8
        dest_node_id = 24
        astar = AStar(map_40, start_node_id, dest_node_id)
        self.assertEqual(astar.search(), [8, 14, 16, 37, 12, 17, 10, 24])

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAStar)
    unittest.TextTestRunner(verbosity=2).run(suite)