import sys
def longest_common_subsequence_recursive(x, y, m, n):
    if m == 0 or n == 0: return 0
    if x[m - 1] == y[n - 1]:
        return longest_common_subsequence_recursive(x, y, m - 1, n - 1) + 1
    else:
        return max(longest_common_subsequence_recursive(x, y, m - 1, n), longest_common_subsequence_recursive(x, y, m, n - 1))

def longest_common_subsequence(x, y):
    row = [0] * (len(y) + 1)
    d = []
    for i in range(0, len(x) + 1):
        d.append(row[0:])
    for i in range(1, len(x) + 1):
        for j in range(1, len(y) + 1):
            diag = d[i - 1][j - 1] + (1 if x[i - 1] == y[j - 1] else 0)
            d[i][j] = max(d[i - 1][j], d[i][j -1], diag)
    return d[-1][-1]

def longest_common_subsequence_of_3_sequence(x, y, z):
    for i in range(0, len(x) + 1):
        for j in range(0, len(y) + 1):
            d = [[[0 for k in range(0, len(z) + 1)] for j in range(0, len(y) + 1)] for i in range(0, len(x) + 1)]

    for i in range(1, len(x) + 1):
        for j in range(1, len(y) + 1):
            for k in range(1, len(z) + 1):
                diag = d[i - 1][j - 1][k - 1] + (1 if x[i - 1] == y[j - 1] and y[j - 1] == z[k - 1] else 0)
                d[i][j][k] = max(d[i - 1][j][k], d[i][j -1][k], d[i][j][k - 1], diag)
    return d[-1][-1][-1]

if __name__ == '__main__':
    print(longest_common_subsequence("ABCBDAB", "BDCABA"))
    print(longest_common_subsequence_of_3_sequence("ABCBDAB", "BDCABA", "BADACB"))
