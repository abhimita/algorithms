import sys
import unittest

# Find a highest-scoring overlap alignment between two strings.
# Input: A match score m, a mismatch penalty μ, a gap penalty σ, and two DNA strings s and t.
# Output: The maximum alignment score of an overlap alignment between s and t followed by an overlap
# alignment achieving this maximum score.
# Biologists use overlapping reads to assemble a genome, a problem that is complicated by errors in reads.
# To find overlaps between error-prone reads, we define an overlap alignment of strings s = s1 ... sn
# and t = t1 ... tm as a global alignment of a suffix of s with a prefix of t. An optimal overlap
# alignment of strings s and t maximizes the global alignment score between an i-suffix of s and a
# j-prefix of t (i.e., between si ... sn and t1 ... tj) among all i and j.
# Input Format. The first line of the input contains m followed by μ followed by σ (separated by spaces),
# the second line of the input contains a DNA string s, and the third line of the input contains a DNA
# string t.
# Output Format. The first line of the output should contain the maximum score of an overlap alignment between s and t, and the next two lines should contain an overlap alignment between a suffix of s and a prefix of t achieving this maximum score. Specifically, the second line should contain a suffix of s with gaps placed appropriately, and the third line should contain a prefix of t with gaps placed appropriately.

def print_cost_matrix(dp):
    for i in range(0, len(dp)):
        for j in range(0, len(dp[i])):
            print(dp[i][j], end=' ')
        print()

def align(m, mu, sigma, s, t):
    row = [(0, 0) for _ in range(len(s) + 1)]
    dp = [row[0:] for _ in range(len(t) + 1)]
    for j in range(1, len(s) + 1):
        dp[0][j] = (0, 0)
    for i in range(1, len(t) + 1):
        dp[i][0] = (dp[i - 1][0][0] - sigma, (i - 1) * (len(s) + 1) + 0)

    max_value = float('-inf')
    max_i = -1
    for i in range(1, len(t) + 1):
        for j in range(1, len(s) + 1):
            dp[i][j] = (max(dp[i - 1][j][0] - sigma,
                            dp[i][j - 1][0] - sigma,
                            dp[i - 1][j - 1][0] + (m if s[j - 1] == t[i - 1] else -mu)
                            ), None)
            if j == len(s) and max_value < dp[i][j][0]:
                max_value = dp[i][j][0]
                max_i = i
            if dp[i][j][0] == dp[i - 1][j - 1][0] + (m if s[j - 1] == t[i - 1] else -mu):
                dp[i][j] = (dp[i][j][0], (i - 1) * (len(s) + 1) + j - 1)
            elif dp[i][j][0] == dp[i][j - 1][0] - sigma:
                dp[i][j] = (dp[i][j][0], i * (len(s) + 1) + j - 1)
            elif dp[i][j][0] == dp[i - 1][j][0] - sigma:
                dp[i][j] = (dp[i][j][0], (i - 1) * (len(s) + 1) + j)

    i = max_i
    j = len(s)
    path = [i * (len(s) + 1) + j]
    while i > 0 and j > 0:
        path.append(dp[i][j][1])
        i, j = dp[i][j][1] // (len(s) + 1), dp[i][j][1] % (len(s) + 1)

    path.reverse()
    first_string = []
    second_string = []
    for index, p in enumerate(path):
        i, j = p // (len(s) + 1), p % (len(s) + 1)
        if index == 0:
            if i > 0:
                second_string.extend(t[:i])
                first_string.extend('-' * len(t[:i]))
                continue
        prev_i, prev_j = path[index - 1] // (len(s) + 1), path[index - 1] % (len(s) + 1)
        if i - prev_i == 1 and j - prev_j == 1:
            if dp[i][j][0] != dp[prev_i][prev_j][0]:
                second_string.append(t[prev_i])
                first_string.append(s[prev_j])
        elif i - prev_i == 0 and j - prev_j == 1:
            second_string.append('-')
            first_string.append(s[prev_j])
        elif i - prev_i == 1 and j - prev_j == 0:
            second_string.append(t[prev_i])
            first_string.append('-')
    return str(max_value) + '\n' + ''.join(first_string) + '\n' + ''.join(second_string)

class TestOverlapAlignment(unittest.TestCase):

    def test_base_case(self):
        assert align(m=1, mu=1, sigma=2, s='GAGA', t='GAT') == '2\nGA\nGA'

    def test_matrix_initialization(self):
        assert align(m=1, mu=1, sigma=1, s='CCAT', t='AT') == '2\nAT\nAT'

    def test_correctness_of_indel_penalization(self):
        assert align(m=1, mu=5, sigma=1, s='GAT', t='CAT') == '1\n-AT\nCAT'

    def test_to_confirm_local_or_fitting_alignment_is_not_used(self):
        assert align(m=1, mu=5, sigma=1, s='ATCACT', t='AT') == '1\nACT\nA-T'

    def test_that_end_characters_are_ignore_for_better_score(self):
        assert align(m=1, mu=1, sigma=5, s='ATCACT', t='ATG') == '0\nCT\nAT'

    def test_when_first_string_is_longer_than_second(self):
        assert align(m=3, mu=2, sigma=1, s='CAGAGATGGCCG', t='ACG') == '5\nATGGCCG\nA----CG'

    def test_when_second_string_is_longer_than_first(self):
        assert align(m=2, mu=3, sigma=1, s='CTT', t='AGCATAAAGCATT') == '0\n--C-TT\nAGCA-T'

unittest.main(argv=[''], verbosity=2, exit=False)

