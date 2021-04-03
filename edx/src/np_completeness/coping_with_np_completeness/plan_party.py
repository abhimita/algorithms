#uses python3

import sys
import threading

# This code is used to avoid stack overflow issues
sys.setrecursionlimit(10**7) # max depth of recursion
threading.stack_size(2**29)  # new thread will get stack of such size

class Node:
    def __init__(self, weight):
        self.weight = weight
        self.children = []

def ReadTree():
    size = int(input())
    tree = [None] + [Node(w) for w in map(int, input().split())]
    for i in range(1, size):
        a, b = list(map(int, input().split()))
        tree[a].children.append(b)
        tree[b].children.append(a)
    return tree


def dfs(tree, root, parent, max_value):
    if max_value[root] == -1:
        if parent != 0 and len(tree[root].children) == 1:
            max_value[root] = tree[root].weight
        else:
            value_wo_root = 0
            for child in tree[root].children:
                if child != parent:
                    value_wo_root += dfs(tree, child, root, max_value)
            value_w_root = tree[root].weight
            for child in tree[root].children:
                if child != parent:
                    for grand_child in tree[child].children:
                        if grand_child != root:
                            value_w_root += dfs(tree, grand_child, child, max_value)
            max_value[root] = max(value_w_root, value_wo_root)
    return max_value[root]

def MaxWeightIndependentTreeSubset(tree):
    size = len(tree)
    if size == 0:
        return 0
    max_value = [-1] * (size + 1)
    dfs(tree, 1, 0, max_value)
    return max_value[1]

def main():
    tree = ReadTree();
    weight = MaxWeightIndependentTreeSubset(tree);
    print(weight)

threading.Thread(target=main).start()