#Uses python3
import sys
import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return '(' + str(self.x) + ',' + str(self.y) + ')'

    def get_distance(self, p):
        return math.sqrt((self.x - p.x) ** 2 + (self.y - p.y) ** 2)

class DisjointSet:
    def __init__(self, n):
        self.parent = [i for i in range(n)]
        self.rank = [0] * n
    def find(self, i):
        if self.parent[i] == i:
            return i
        else:
            return self.find(self.parent[i])
    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        elif self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] + 1

def minimum_distance(x, y):
    vertices = []
    for i in range(len(x)):
        vertices.append(Point(x[i], y[i]))
    union_find = DisjointSet(len(vertices))
    edges = []
    for i, s in enumerate(vertices):
        for j, d in enumerate(vertices):
            if j < i:
                edges.append((i, j, s.get_distance(d)))
            else:
                break
    spanning_tree_edges = []
    i = 0
    all_edges = sorted(edges, key=lambda x: x[2])
    min_distance = 0.0
    while len(spanning_tree_edges) < len(vertices) - 1:
        e = all_edges[i]
        x = union_find.find(e[0])
        y = union_find.find(e[1])
        if x != y:
            spanning_tree_edges.append(e)
            union_find.union(x, y)
            min_distance += e[2]
        i += 1
    return min_distance

if __name__ == '__main__':
    #input = sys.stdin.read()
    #data = list(map(int, input.split()))
    data = [4, 0, 0, 0, 1, 1, 0, 1, 1]
    data = [5, 0, 0, 0, 2, 1, 1, 3, 0, 3, 2]
    n = data[0]
    x = data[1::2]
    y = data[2::2]
    print("{0:.9f}".format(minimum_distance(x, y)))
