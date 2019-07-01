from heap_node import HeapNode
import unittest
from binary_heap import BinaryHeap

class TestBinaryHeap(unittest.TestCase):
    def setup(self, names, values):
        return [HeapNode({'name': n[0], 'value': n[1]}, 'value') for n in zip(names, values)]

    # Test building heap when the node values are sorted
    def test_build_heap_with_sorted_list(self):
        values = [1, 3, 5, 7, 9, 10, 11]
        names = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        binary_heap = BinaryHeap(self.setup(names, values))
        binary_heap.build_heap()
        self.assertEqual([x.get_value_attribute() for x in binary_heap.node_list if x is not None], [1, 3, 5, 7, 9, 10, 11])

    # Test building heap when node values are reverse sorted
    def test_build_heap_with_reverse_sorted_list(self):
        names = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        values = [11, 10, 9, 7, 5, 3, 1]
        binary_heap = BinaryHeap(self.setup(names, values))
        binary_heap.build_heap()
        self.assertEqual([x.get_value_attribute() for x in binary_heap.node_list if x is not None], [1,5,11,7,10,3,9])

    # Test deletion of root node and rebalancing the tree
    def test_delete_min(self):
        names = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        values = [5, 3, 7, 1, 9, 10, 11]
        binary_heap = BinaryHeap(self.setup(names, values))
        binary_heap.build_heap()
        self.assertEqual([x.get_value_attribute() for x in binary_heap.node_list if x is not None], [1, 3, 7, 5, 9, 10, 11])
        self.assertEqual(binary_heap.delete_min().get_value_attribute(), 1)

    # Test updating the value of a non-leaf node
    def test_update_with_lower_value_for_non_leaf_node(self):
        values = [1, 3, 5, 7, 9, 10, 11]
        names = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        binary_heap = BinaryHeap(self.setup(names, values))
        binary_heap.build_heap()
        binary_heap.update(2, 0)
        self.assertEqual([x.get_value_attribute() for x in binary_heap.node_list if x is not None], [0, 1, 5, 7, 9, 10, 11])

    def test_update_with_lower_value_for_leaf_node(self):
        values = [1, 3, 5, 7, 9, 10, 11]
        names = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        binary_heap = BinaryHeap(self.setup(names, values))
        binary_heap.build_heap()
        binary_heap.update(6, 4)
        self.assertEqual([x.get_value_attribute() for x in binary_heap.node_list if x is not None], [1, 3, 4, 7, 9, 5, 11])

    def test_insert_nodes_with_descending_values(self):
        binary_heap = BinaryHeap()
        binary_heap.insert(HeapNode({'name': 'A', 'value': 0.91}, 'value'))
        self.assertEqual([x.get_value_attribute() for x in binary_heap.node_list if x is not None], [0.91])
        binary_heap.insert(HeapNode({'name': 'B', 'value': 0.57}, 'value'))
        self.assertEqual([x.get_value_attribute() for x in binary_heap.node_list if x is not None], [0.57, 0.91])
        binary_heap.insert(HeapNode({'name': 'B', 'value': 0.34}, 'value'))
        self.assertEqual([x.get_value_attribute() for x in binary_heap.node_list if x is not None], [0.34, 0.91, 0.57])

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBinaryHeap)
    unittest.TextTestRunner(verbosity=2).run(suite)