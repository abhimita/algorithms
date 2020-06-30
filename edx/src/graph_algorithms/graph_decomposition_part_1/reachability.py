
import sys

def reach(adj, x, y):
    visited = [False] * len(adj)
    stack = []
    stack.append(x)
    visited[x] = True
    while len(stack) > 0:
        n = stack.pop(len(stack) - 1)
        if n == y:
            return 1
        else:
            for neighbor in adj[n]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    stack.append(neighbor)
    return 0


if __name__ == '__main__':
    #input = sys.stdin.read()
    #data = list(map(int, input.split()))
    data = [8, 7, 1, 2, 1, 3, 2, 5, 6, 6, 2, 6, 5, 7, 6, 8, 7, 8]
    data = [4, 4, 1, 2, 3, 2, 4, 3, 1, 4, 1, 4]
    data = [4, 2, 1, 2, 3, 2, 1, 4]
    data = [2, 0, 1, 2]
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))
    x, y = data[2 * m:]
    adj = [[] for _ in range(n)]
    x, y = x - 1, y - 1
    for (a, b) in edges:
        adj[a - 1].append(b - 1)
        adj[b - 1].append(a - 1)
    print(reach(adj, x, y))