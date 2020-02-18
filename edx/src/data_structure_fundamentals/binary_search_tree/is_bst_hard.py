#!/usr/bin/python3

import sys, threading

sys.setrecursionlimit(10**7) # max depth of recursion
threading.stack_size(2**27)  # new thread will get stack of such size

class BinaryTreeWithDuplicateValue:
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

    def isBST(self, root_index=0, min_value=float('-inf'), max_value=float('inf')):
        if root_index == -1:
            return True
        if self.key[root_index] < min_value or self.key[root_index] > max_value:
            return False
        else:
            return self.isBST(self.left[root_index], min_value, self.key[root_index] - 1) and self.isBST(self.right[root_index], self.key[root_index], max_value)

def IsBinarySearchTree(tree):
    return tree.isBST()

def main():
    tree = BinaryTreeWithDuplicateValue()
    tree.read()
    if tree.n == 0:
        print("CORRECT")
    else:
        is_bst = IsBinarySearchTree(tree)
        print("CORRECT" if is_bst else "INCORRECT")

threading.Thread(target=main).start()

