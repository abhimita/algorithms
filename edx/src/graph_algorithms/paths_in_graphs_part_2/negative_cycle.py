#Uses python3

import sys

# Bellman Ford algorithm with negative weights
def bellman_ford_negative_cycle(node_count, edge_cost, s):
    dist = [float('inf') for i in range(node_count)]
    dist[s] = 0
    for i in range(0, node_count):
        # Optimization to bail out if none of the element in distance array is updated
        any_distance_updated = False
        for e in edge_cost:
            if dist[e[0]] + e[2] < dist[e[1]]:
                any_distance_updated = True
                dist[e[1]] = dist[e[0]] + e[2]
        if not any_distance_updated: break
    for e in edge_cost:
        if dist[e[0]] + e[2] < dist[e[1]]:
            return 1
    return 0

def negative_cycle(adj, cost):
    edge_cost = []
    source_vertices = set()
    for s in range(len(adj)):
        for i, t in enumerate(adj[s]):
            edge_cost.append([s, t, cost[s][i]])
            # Pick up source vertex with negative weights
            if cost[s][i] < 0:
                source_vertices.add(s)
    result = 0
    for s in source_vertices:
        result = bellman_ford_negative_cycle(len(adj), edge_cost, s)
        if result == 1:
            return result
    return result

if __name__ == '__main__':
    #input = sys.stdin.read()
    #data = list(map(int, input.split()))

    #data = [4, 4, 1, 2, -5, 4, 1, 2, 2, 3, 2, 3, 1, 1]
    #data = [3, 3, 1, 2, 7, 1, 3, 5, 2, 3, 2]
    #data = [8, 13, 1, 2, 4, 2, 6, 3, 1, 3, 4, 3, 6, -2, 4, 1, 3, 4, 3, 2, 3, 5, 4, 5, 4, 1, 6, 5, -3, 5, 7, -2, 7, 8, 2, 8, 5, -2, 6, 2, 3]
    data = [6, 9, 1, 2, 20, 2, 3, 33, 3, 4, 7, 1, 5, 10, 5, 6, 50, 6, 4, -2, 2, 6, 20, 6, 3, -20, 5, 3, 10]
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(zip(data[0:(3 * m):3], data[1:(3 * m):3]), data[2:(3 * m):3]))
    data = data[3 * m:]
    adj = [[] for _ in range(n)]
    cost = [[] for _ in range(n)]
    for ((a, b), w) in edges:
        adj[a - 1].append(b - 1)
        cost[a - 1].append(w)
    print(negative_cycle(adj, cost))