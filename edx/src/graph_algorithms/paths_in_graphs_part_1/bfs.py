import sys
import queue

def distance(adj, s, t):
    dist = [float('inf')] * len(adj)
    q = queue.SimpleQueue()
    q.put(s)
    dist[s] = 0
    while not q.empty():
        n = q.get()
        for nbr in adj[n]:
            if dist[nbr] == float('inf'):
                q.put(nbr)
                dist[nbr] = dist[n] + 1
    return(dist[t] if dist[t] != float('inf') else -1)

if __name__ == '__main__':
    #input = sys.stdin.read()
    #data = list(map(int, input.split()))
    data = [4, 4, 1, 2, 4, 1, 2, 3, 3, 1, 2, 4]
    #data = [5, 4, 5, 2, 1, 3, 3, 4, 1, 4, 3, 5]
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))
    adj = [[] for _ in range(n)]
    for (a, b) in edges:
        adj[a - 1].append(b - 1)
        adj[b - 1].append(a - 1)
    s, t = data[2 * m] - 1, data[2 * m + 1] - 1
    print(distance(adj, s, t))
