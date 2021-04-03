# python3
import unittest

# Find the length of a longest path in a rectangular grid.
# Input: Integers n and m, an n × (m+1) matrix Down, and an (n+1) × m matrix Right.
# Output: The length of a longest path from source (0, 0) to sink (n, m) in the n × m rectangular
#         grid whose edge weights are defined by the matrices Down and Right.
# Imagine you are a tourist in Midtown Manhattan, and you want to see as many sights as possible
# on your way from the corner of 59th Street and 8th Avenue to the corner of 42nd Street and
# 3rd Avenue (Figure below). However, you are short on time, and at each intersection, you can
# only move south (↓) or east (→). You can choose from many different paths through the map,
# but no path will visit all the sights. The challenge of finding a legal path through the city
# that visits the most sights is called the Manhattan Tourist Problem.

# Input Format. The first line of the input contains the integers n and m (separated by a space).
# The next n lines (each with m + 1 space-delimited numbers) represent the matrix Down.
# The next line is the “-” symbol (to separate the matrices Down and Right).
# The next n + 1 lines (each with m space-delimited numbers) represent the matrix Right.

# Output Format. The length of a longest path from source (0, 0) to sink (n, m) in the n × m
# rectangular grid whose edge lengths are defined by the matrices Down and Right.
# Constraints. 1 ≤ n ≤ 20; 1 ≤ m ≤ 20


def longest_path(n, m, down, right):
    row = [0] * len(down[0])
    matrix = [row[0:] for _ in right]
    for i in range(1, len(matrix)):
        matrix[i][0] = matrix[i - 1][0] + down[i - 1][0]
    for j in range(1, len(matrix[0])):
        matrix[0][j] = matrix[0][j - 1] + right[0][j - 1]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            matrix[i][j] = max(matrix[i - 1][j] + down[i - 1][j], matrix[i][j - 1] + right[i][j - 1])
    return matrix[n][-1]


class TestLongestPath(unittest.TestCase):
    def test_base_case(self):
        n, m = 4, 4
        down = [
            [1, 0, 2, 4, 3],
            [4, 6, 5, 2, 1],
            [4, 4, 5, 2, 1],
            [5, 6, 8, 5, 3]
        ]
        right = [
            [3, 2, 4, 0],
            [3, 2, 4, 2],
            [0, 7, 3, 3],
            [3, 3, 0, 2],
            [1, 3, 2, 2]
        ]
        assert longest_path(n, m, down, right) == 34

    def test_edge_case_for_first_column_down_and_last_row_right(self):
        n = 2
        m = 2
        down = [
            [20, 0, 0],
            [20, 0, 0]
        ]
        right = [
            [0, 0],
            [0, 0],
            [10, 10]
        ]
        assert longest_path(n, m, down, right) == 60

    def test_edge_case_for_last_column_down_and_first_row_right(self):
        n = 2
        m = 2
        down = [
            [0, 0, 20],
            [0, 0, 20]
        ]
        right = [
            [10, 10],
            [0, 0],
            [0, 0]
        ]
        assert longest_path(n, m, down, right) == 60

    def test_greedy_algorithm_is_not_used(self):
        n = 2
        m = 2
        down = [
            [20, 0, 0],
            [0, 0, 0]
        ]
        right = [
            [0, 30],
            [0, 0],
            [0, 0]
        ]
        assert longest_path(n, m, down, right) == 30

    def test_unequal_row_and_column_count(self):
        n = 5
        m = 3
        down = [
            [20, 5, 0, 10],
            [0, 5, 10, 0],
            [10, 10, 0, 15],
            [0, 20, 20, 25],
            [30, 10, 5, 30]
        ]
        right = [
            [0, 30, 15],
            [10, 20, 10],
            [10, 10, 20],
            [20, 25, 30],
            [15, 35, 40],
            [15, 10, 25]
        ]
        assert longest_path(n, m, down, right) == 175

    def test_where_column_count_more_than_row_count(self):
        n = 3
        m = 5
        down = [
            [0, 5, 10, 0, 10, 10],
            [15, 0, 20, 20, 25, 30],
            [10, 5, 30, 15, 0, 20]
        ]
        right = [
            [0, 30, 15, 10, 20],
            [10, 10, 10, 20, 20],
            [25, 30, 15, 35, 40],
            [15, 10, 25, 15, 20]
        ]
        assert longest_path(n, m, down, right) == 180


unittest.main(argv=[''], verbosity=2, exit=False)
