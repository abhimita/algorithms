import unittest

def edit_distance(s, t):
    row = [0 for _ in range(len(s) + 1)]
    dp = [row[0:] for _ in range(len(t) + 1)]
    for j in range(1, len(s) + 1):
        dp[0][j] = dp[0][j - 1] + 1
    for i in range(1, len(t) + 1):
        dp[i][0] = dp[i - 1][0] + 1
    for i in range(1, len(t) + 1):
        for j in range(1, len(s) + 1):
            dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + (0 if s[j - 1] == t[i - 1] else 1))
    return dp[len(t)][len(s)]

class TestEditDistance(unittest.TestCase):
    def test_base_case(self):
        assert edit_distance(s='GAGA', t='GAT') == 2

    def test_if_two_strings_are_same(self):
        assert edit_distance(s='AC', t='AC') == 0

    def test_when_edit_distance_includes_deletion_substitution(self):
        assert edit_distance(s='AT', t='G') == 2

    def test_when_first_string_is_larger_than_second_string(self):
        assert edit_distance(s='CAGACCGAGTTAG', t='CGG') == 10

    def test_when_second_string_is_larger_than_first_string(self):
        assert edit_distance(s='CGT', t='CAGACGGTGACG') == 9

unittest.main(argv=[''], verbosity=2, exit=False)