import sys


def acyclic(adj):
    visited = [False] * len(adj)
    in_recursion_stack = [False] * len(adj)
    # every element in flag array can have one of the three allowable values
    # 0 -> not visited
    # 1 -> visited and in stack
    # 2 -> visited and popped out of stack

    def isCycle(node):
        visited[node] = True
        in_recursion_stack[node] = True
        for nbr in adj[node]:
            if not visited[nbr]:
                if isCycle(nbr) == True:
                    return True
            elif in_recursion_stack[nbr] == True:
                return True
        in_recursion_stack[node] = False
        return False

    for n in range(len(adj)):
        if not visited[n]:
            if isCycle(n):
                return 1
    return 0


if __name__ == '__main__':
    #input = sys.stdin.read()
    #data = list(map(int, input.split()))
    #data = [5, 6, 1, 2, 1, 3, 2, 4, 4, 5, 5, 2]
    data = [5, 7, 1, 2, 2, 3, 1, 3, 3, 4, 1, 4, 2, 5, 3, 5]
    data = [6, 7, 1, 2, 2, 3, 3, 4, 1, 3, 1, 6, 6, 5, 5, 3]
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))
    adj = [[] for _ in range(n)]
    for (a, b) in edges:
        adj[a - 1].append(b - 1)
    print(acyclic(adj))