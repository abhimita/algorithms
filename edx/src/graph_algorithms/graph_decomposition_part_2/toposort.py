import sys

def toposort(adj):
    stack = []
    visited = [False] * len(adj)
    def topological_sort(n):
        visited[n] = True
        for nbr in adj[n]:
            if not visited[nbr]:
                topological_sort(nbr)
        stack.append(n)

    for n in range(len(adj)):
        if not visited[n]:
            topological_sort(n)
    stack.reverse()
    return stack

if __name__ == '__main__':
#    input = sys.stdin.read()
#    data = list(map(int, input.split()))
    data = [6, 6, 6, 1, 5, 1, 5, 2, 4, 2, 3, 4, 6, 3]
    data = [4, 3, 1, 2, 4, 1, 3, 1]
    data = [4, 1, 3, 1]
    data = [5, 7, 2, 1, 3, 2, 3, 1, 4, 3, 4, 1, 5, 2, 5, 3]
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))
    adj = [[] for _ in range(n)]
    for (a, b) in edges:
        adj[a - 1].append(b - 1)
    order = toposort(adj)
    for x in order:
        print(x + 1, end=' ')

