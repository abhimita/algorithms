import sys
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(0, n + 1))
        self.parent[0] = -1 # this cell is not used
        self.rank = [0] * len(self.parent)

    def find(self, i):
        while i != self.parent[i]:
            i = self.parent[i]
        return(i)

    def find_with_path_compression(self, i):
        if i != self.parent[i]:
            self.parent[i] = self.find_with_path_compression(self.parent[i])
        return(self.parent[i])

    def merge(self, i, j):
        i_parent = self.find(i)
        j_parent = self.find(j)
        if i_parent == j_parent:
            return
        if self.rank[i_parent] > self.rank[j_parent]:
            self.parent[j_parent] = i_parent
        else:
            self.parent[i_parent] = j_parent
            if self.rank[i_parent] == self.rank[i_parent]:
                self.rank[j_parent] += 1

if __name__ == '__main__':
    union_find = UnionFind(9)
    union_find.merge(6, 8)
    union_find.merge(6, 1)
    union_find.merge(4, 2)
    union_find.merge(4, 3)
    union_find.merge(9, 7)
    union_find.merge(4, 9)
    print(union_find.parent)
    union_find.find_with_path_compression(9)
    print(union_find.parent)
