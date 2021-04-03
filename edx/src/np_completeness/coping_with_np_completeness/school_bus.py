# python3

INF = float('inf')

def read_data():
    n, m = map(int, input().split())
    graph = [[INF] * n for _ in range(n)]
    for _ in range(m):
        u, v, weight = map(int, input().split())
        u -= 1
        v -= 1
        graph[u][v] = graph[v][u] = weight

    return graph

def optimal_path(graph):

    n = len(graph)
    VISITED = (1 << n) - 1

    row = [(-1, -1) for _ in range(0, n)]
    dp = [row[0:] for _ in range(0, 1 << n)]
    for i in range(1, n):
        dp[VISITED][i] = (graph[0][i], i)

    def tsp_dyn(mask, pos):
        if dp[mask][pos][0] != -1:
            return dp[mask][pos]
        else:
            min_cost = INF
            min_index = -1
            for city in range(0, n):
                if (mask & (1 << city)) == 0:
                    cost = graph[pos][city] + tsp_dyn(mask | (1 << city), city)[0]
                    if cost < min_cost:
                        min_cost = cost
                        min_index = city

            dp[mask][pos] = (min_cost, min_index)
            return dp[mask][pos]

    tsp_dyn(1, 0)

    cost = dp[1 << 0][0][0]
    if cost == INF:
        return -1, []

    node = prev_node = 0
    path = [node + 1]
    mask = 1 << node
    for _ in range(0, n - 1):
        prev_node = dp[mask][prev_node][1]
        path.append(prev_node + 1)
        mask = mask | (1 << prev_node)
    return cost, path


def print_answer(path_weight, path):
    print(path_weight)
    if path_weight == -1:
        return
    print(' '.join(map(str, path)))


if __name__ == '__main__':
    print_answer(*optimal_path(read_data()))