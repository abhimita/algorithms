"""
Binary heap implementation in Python
"""
class BinaryHeap:
    def __init__(self, node_list=[]):
        self.node_list = []
        # First position in the array is set aside and we will start storing data from node_list[1]
        # This is done to make sure that following heap formulas work without any change
        # If the parent node is in position i then its two children will be 2 * i and 2 * 1 + 1
        # in case the node has both children
        # Conversely, parent of node at i is at i // 2
        self.node_list.append(None)
        self.node_list.extend(node_list)
        self.size = len(node_list)

    # This method is called when a node is inserted in the heap at the last empty position
    # That insertion can destroy the property of the heap that node value of the parent is less (more)
    # than the node value of any of its left and right substree for min/max heap
    def _percolate_up(self, i):
        while i // 2 >= 1 and self.node_list[i // 2].get_value_attribute() > self.node_list[i].get_value_attribute():
            self.node_list[i // 2], self.node_list[i] = self.node_list[i], self.node_list[i // 2]
            i = i // 2

    # This method is invoked when min(max) value in removed from topmost root node in the heap
    # Along with that removal, we use the last tree node to replace the root node
    # As it may destroy the heap property, so it is pushed down below till the property is restored
    def _percolate_down(self, i):
        while i * 2 <= self.size:
            j = self._min_child(i)
            if self.node_list[i].get_value_attribute() > self.node_list[j].get_value_attribute():
                self.node_list[i], self.node_list[j] = self.node_list[j], self.node_list[i]
            i = j

    # Get the index of the child having minimum value
    def _min_child(self, i):
        if 2 * i + 1 > self.size:
            return 2 * i
        else:
            if self.node_list[2 * i].get_value_attribute() < self.node_list[2 * i + 1].get_value_attribute():
                return 2 * i
            else:
                return 2 * i + 1

    def delete_min(self):
        min_value = self.node_list[1]
        # Make the last node, the root of the heap
        self.node_list[1] = self.node_list[-1]
        # Remove the last node
        self.node_list.pop(-1)
        # Decrement the size of the heap
        self.size -= 1
        # Push down the node to balance
        self._percolate_down(1)
        return min_value

    def insert(self, node):
        # Empty position to make the array conform to the rules of locating parent index from children node
        self.size += 1
        self.node_list.append(node)
        self._percolate_up(self.size)

    def update(self, i, value):
        self.node_list[i].set_value_attribute(value)
        self._percolate_up(i)

    def build_heap(self):
        for i in range(self.size // 2, 0, -1):
            j = self._min_child(i)
            if self.node_list[i].get_value_attribute() > self.node_list[j].get_value_attribute():
                self.node_list[i], self.node_list[j] = self.node_list[j], self.node_list[i]
        # Root node already contains minimum value. But the last swap may be resulted in violation of heap
        # property either node at position 2 or 3. An example is before the last swap, the top of the tree
        # looks like following
        # 5 --> 1 --> 3
        #       | --> 9
        # | --> 7 --> 10
        #       | --> 11
        # Last swap will push the node with value 1 to the root position
        # 1 --> 5 --> 3
        #       | --> 9
        # | --> 7 --> 10
        #       | --> 11
        self._percolate_down(2)

    def __str__(self):
        return ','.join([str(n) for index, n in enumerate(self.node_list) if index > 0])
