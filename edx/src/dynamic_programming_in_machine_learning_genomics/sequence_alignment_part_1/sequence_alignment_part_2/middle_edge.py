#python3
import sys
import unittest

# Find a middle edge in the alignment graph in linear space.
# Input: A match score m, a mismatch penalty μ, a gap penalty σ, and two DNA strings s and t.
# Output: The maximum alignment score of s and t followed by an alignment achieving this
# maximum score.
# The quadratic memory required to store the entire alignment matrix can become overly
# massive for long DNA strings. However, keep in mind that, during the alignment algorithm,
# we only need two rows (i.e., linear space) at any given time in order to compute the optimal
# score. It turns out that we can exploit this phenomenon to compute the entire optimal
# alignment in linear space as well.
# Given strings s1 … sn and and t1 … tm, define middle = ⌊m/2⌋. The middle column of the
# alignment graph of s and t is the column containing all nodes (i, middle) for 0 ≤ i ≤ n.
# A longest path from source to sink in the alignment graph must cross the middle column
# somewhere, and we refer to the node on a longest path belonging to the middle column as
# a middle node, and we refer to the edge in an optimal path starting at a given middle
# node as a middle edge.

# Input Format. The first line of the input contains m followed by μ followed by σ (separated
# by spaces), the second line of the input contains a DNA string s, and the third line of
# the input contains a DNA string t.

# Output Format. The middle edge in the form (i,j) (k,l), where (i,j) and (k, l) are adjacent
# nodes in the alignment graph, i.e., there is an edge between these nodes.

def score(m, mu, sigma, s, t):
    row = [0 for _ in range(0, 2)]
    dp = [row[0:] for _ in range(0, len(t) + 1)]
    for i in range(1, len(t) + 1):
        dp[i][0] = dp[i - 1][0] - sigma
        dp[i][1] = dp[i][0]
    #dp[0][1] = -sigma

    for j in range(1, len(s) + 1):
        for i in range(1, len(t) + 1):
            dp[i][1] = max(dp[i - 1][1] - sigma,
                           dp[i][0] - sigma,
                           dp[i - 1][0] + (m if s[j - 1] == t[i - 1] else -mu))

        if j != len(s):
            for k in range(0, len(t) + 1):
                dp[k][0] = dp[k][1]
            dp[0][1] = dp[0][0] - sigma
    return dp

def backtrack(dp, n, m , mu, sigma, s, t):
    max_value = max(
        (dp[n - 1][1] - sigma) if n - 1 >= 0 else float('-inf'),
        dp[n][0] - sigma,
        (dp[n - 1][0] + (m if s[-1] == t[n - 1] else -mu)) if n - 1 >= 0 else float('-inf'))
    if max_value == ((dp[n - 1][0] + (m if s[-1] == t[n - 1] else -mu)) if n - 1 >= 0 else float('-inf')):
        return 'D'
    elif max_value == (dp[n][0] - sigma):
        return 'H'
    else:
        return 'V'

def middle_edge(m, mu, sigma, s, t):
    mid = len(s) // 2
    left_columns = score(m, mu, sigma, s[:mid], t)
    right_columns = score(m, mu, sigma, ''.join(list(reversed(s[mid:]))), ''.join(list(reversed(t))))

    mid_column = list(map(lambda x: x[0] + x[1],
                          zip([r[1] for r in left_columns],
                              list(reversed([r[1] for r in right_columns])))))
    row_number = mid_column.index(max(mid_column))
    column_number = len(s) // 2

    middle_edge_dir = backtrack(right_columns, len(t) - row_number, m , mu, sigma, list(reversed(s[mid:])), list(reversed(t)))
    current_node = (row_number, len(s) // 2)
    if middle_edge_dir == 'D':
        next_node = (row_number + 1, column_number + 1)
    elif middle_edge_dir == 'H':
        next_node = (row_number, column_number + 1)
    else:
        next_node = (row_number + 1, column_number)
    return (str(current_node) + ' ' + str(next_node))

class TestMiddleEdge(unittest.TestCase):

    # Test data from https://en.wikipedia.org/wiki/Hirschberg%27s_algorithm
    def test_wikipedia_case(self):
        assert middle_edge(m=2, mu=1, sigma=2, s='TATGC', t='AGTACGCA') == '(4, 2) (5, 3)'

    def test_base_case(self):
        assert middle_edge(m=1, mu=1, sigma=2, s='GAGA', t='GAT') == '(2, 2) (3, 3)'

    def test_detection_of_horizontal_middle_edge(self):
        assert middle_edge(m=1, mu=5, sigma=1, s='TTTT', t='CC') == '(0, 2) (0, 3)'

    def test_finding_middle_edge_when_first_string_is_odd_length(self):
        assert middle_edge(m=1, mu=1, sigma=2, s='GAT', t='AT') == '(0, 1) (1, 2)'

    def test_finding_vertical_middle_edge(self):
        assert middle_edge(m=1, mu=1, sigma=1, s='TTTT', t='TTCTT') == '(2, 2) (3, 2)'

    def test_when_middle_edge_has_to_horizontal(self):
        assert middle_edge(m=1, mu=5, sigma=1, s='GAACCC', t='G') == '(1, 3) (1, 4)'

    def test_when_match_score_is_not_one(self):
        assert middle_edge(m=2, mu=3, sigma=1, s='ACAGT', t='CAT')  == '(1, 2) (2, 3)'

    def test_when_first_string_is_of_length_one(self):
        assert middle_edge(m=2, mu=5, sigma=3, s='T', t='AATCCC') == '(0, 0) (1, 0)'

unittest.main(argv=[''], verbosity=2, exit=False)
