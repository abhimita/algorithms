# python3

import unittest
from unittest.mock import patch
from io import StringIO
import sys, threading
sys.setrecursionlimit(10**6) # max depth of recursion
threading.stack_size(2**27)  # new thread will get stack of such size

class TreeOrders:
    def read(self):
        self.n = int(sys.stdin.readline())
        self.key = [0 for i in range(self.n)]
        self.left = [0 for i in range(self.n)]
        self.right = [0 for i in range(self.n)]
        for i in range(self.n):
            [a, b, c] = map(int, sys.stdin.readline().split())
            self.key[i] = a
            self.left[i] = b
            self.right[i] = c

    def inOrder(self, root_index=0, level=0):
        if root_index == -1:
            return
        if level == 0:
            self.result = []
        self.inOrder(root_index=self.left[root_index], level=level + 1)
        self.result.append(self.key[root_index])
        self.inOrder(root_index=self.right[root_index], level=level + 1)
        return self.result

    def preOrder(self, root_index=0, level=0):
        if root_index == -1:
            return
        if level == 0:
            self.result = []
        self.result.append(self.key[root_index])
        self.preOrder(root_index=self.left[root_index], level=level + 1)
        self.preOrder(root_index=self.right[root_index], level=level + 1)
        return self.result

    def postOrder(self, root_index=0, level=0):
        if root_index == -1:
            return
        if level == 0:
            self.result = []
        self.postOrder(root_index=self.left[root_index], level=level + 1)
        self.postOrder(root_index=self.right[root_index], level=level + 1)
        self.result.append(self.key[root_index])
        return self.result


def main():
    tree = TreeOrders()
    tree.read()
    print(" ".join(str(x) for x in tree.inOrder()))
    print(" ".join(str(x) for x in tree.preOrder()))
    print(" ".join(str(x) for x in tree.postOrder()))
    sys.exit(0)



class TestTreeOrders(unittest.TestCase):
    # The tree is described in level order
    # First line - node#1 with value=4 has two children. left=node#1 right=node#2
    # Second line - node#2 with value=2 has two children. left=node#3 right=node#4
    # Third line - node#3 with value=6 has two children. left=node#5 right=node#6
    # Fourth line - node#4 with value=1 has no children. (leaf node)
    @patch("sys.stdin",
           StringIO('''7
           4 1 2
           2 3 4
           6 5 6
           1 -1 -1
           3 -1 -1
           5 -1 -1
           7 -1 -1'''))
    def test_tree_order_for_seven_node_tree(self):
        tree = TreeOrders()
        tree.read()
        self.assertEqual(tree.inOrder(), [1,2,3,4,5,6,7])
        self.assertEqual(tree.preOrder(), [4,2,1,3,6,5,7])
        self.assertEqual(tree.postOrder(), [1,3,2,5,7,6,4])

# Comment this line when the unit tests need not be run
unittest.main(argv=[''], verbosity=2, exit=False)

# Uncomment this line when the unit tests need not be run
#threading.Thread(target=main).start()