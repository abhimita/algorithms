#!/usr/bin/env python3

import sys
import threading


def compute_height(n, parents):
    # Replace this code with a faster implementation
    max_height = 0
    parent_child_map = {}
    queue = []
    root = -1
    for index, p in enumerate(parents):
        if p == -1:
            root = index
        else:
            if parent_child_map.get(p, '') == '':
                parent_child_map[p] = [index]
            else:
                parent_child_map[p].append(index)
    queue.append((root, 1))
    max_height = -1
    while len(queue) > 0:
        node, height = queue.pop(0)
        if max_height < height:
            max_height = height
        if parent_child_map.get(node, '') != '':
            for c in parent_child_map[node]:
                queue.append((c, height + 1))
    return max_height


def main():
    #nodes = "4 -1 4 1 1 1"
    n = 5
    nodes = "-1 0 4 0 3"
    parents = list(map(int, nodes.split()))
    print(compute_height(n, parents))

main()