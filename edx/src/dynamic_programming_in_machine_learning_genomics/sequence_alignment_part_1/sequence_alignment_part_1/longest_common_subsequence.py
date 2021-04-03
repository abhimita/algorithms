#python3
import sys
import unittest

def LCS(s, t):
    row = [0 for _ in range(len(s) + 1)]
    dp = [row[0:] for _ in range(len(t) + 1)]
    for i in range(len(t) + 1):
        dp[i][0] = 0
    for j in range(len(s) + 1):
        dp[0][j] = 0

    for i in range(0, len(t)):
        for j in range(0, len(s)):
            if s[j] != t[i]:
                dp[i + 1][j + 1] = max(dp[i + 1][j], dp[i][j + 1])
            else:
                dp[i + 1][j + 1] = dp[i][j] + 1
    i = len(t)
    j = len(s)
    lcs_match = []
    while i > 0 and j > 0:
        if t[i - 1] == s[j - 1]:
            lcs_match.append(t[i - 1])
            i -= 1
            j -= 1
        else:
            if dp[i - 1][j] >= dp[i][j - 1]:
                i -= 1
            else:
                j -= 1
    return ''.join(reversed(lcs_match))

class TestLongestCommonSubsequence(unittest.TestCase):
    def test_base_case(self):
        assert LCS('GACT', 'ATG') == 'AT'

    def test_that_does_not_find_longest_common_substring(self):
        assert LCS('ACTGAG', 'GACTGG') == 'ACTGG'

    def test_reconstruction_for_identical_strings(self):
        assert LCS('AC', 'AC') == 'AC'

    def test_reconstruction_when_only_last_character_of_string_matches(self):
        assert LCS('GGGGT', 'CCCCT') == 'T'

    def test_reconstruction_when_only_last_character_of_string_matches(self):
        assert LCS('GGGGT', 'CCCCT') == 'T'

    def test_when_first_string_is_shorter_than_second(self):
        assert LCS('AA', 'CGTGGAT') == 'A'

    def test_when_first_string_is_longer_than_second(self):
        assert LCS('GGTGACGT', 'CT') == 'CT'

unittest.main(argv=[''], verbosity=2, exit=False)
