import sys
import unittest

# Find a highest-scoring alignment between two strings using only linear space.

# Input: A match score m, a mismatch penalty μ, a gap penalty σ, and two DNA strings s and t.
# Output: The maximum alignment score of s and t followed by an alignment achieving this maximum score.
# You are a Bioinformatician and you you want to compare two very long genes of length n on your fast
# laptop that however has small memory, e.g., 10*n. The score of an alignment is defined as the sum
# of the scores of each position of the alignment, the score of a match is +m, the score of a mismatch
# is -μ, and the score of a gap is -σ. You have already implemented the global alignment problem using
# the quadratic O(n2) memory, Now, you have to do it in O(n) memory,

# Input Format. The first line of the input contains m followed by μ followed by σ (separated by spaces),
# the second line of the input contains a string s, and the third line of the input contains a string t.

# Output Format. The first line of the output should contain the maximum score of an alignment between
# s and t, and the next two lines should contain an alignment achieving this maximum score. Specifically,
# the second line should contain s with gaps placed appropriately, and the third line should contain t
# with gaps placed appropriately.
# Constraints. |s| ≤ 10,000; |t| ≤ 10,000

def score(m, mu, sigma, s, t):
    row = [0 for _ in range(0, 2)]
    dp = [row[0:] for _ in range(0, len(t) + 1)]
    for i in range(1, len(t) + 1):
        dp[i][0] = dp[i - 1][0] - sigma
    dp[0][1] = dp[0][0] - sigma
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

def backtrack(dp, m, mu, sigma, s, t):
    first_string = []
    second_string = []
    i = len(dp) - 1
    j = len(dp[i]) - 1
    while i > 0 or j > 0:
        max_value = max(dp[i - 1][j - 1] + (m if s[j - 1] == t[i - 1] else -mu),
                        dp[i - 1][j] - sigma,
                        dp[i][j - 1] - sigma)
        if s[j - 1] == t[i - 1] or max_value == dp[i - 1][j - 1] - mu:
            first_string.append(s[j - 1])
            second_string.append(t[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] - sigma == max_value:
            first_string.append('-')
            second_string.append(t[i - 1])
            i -= 1
        else:
            first_string.append(s[j - 1])
            second_string.append('-')
            j -= 1
    return ''.join(reversed(first_string)), ''.join(reversed(second_string)), dp[-1][-1]

def align(m, mu, sigma, s, t):
    def align_recursive(m, mu, sigma, s, t):
        first_string = ''
        second_string = ''
        value = 0
        if len(s) == 0:
            for i in range(0, len(t)):
                first_string += '-'
                second_string += t[i]
                value += (-sigma)
        elif len(t) == 0:
            for i in range(0, len(s)):
                first_string += s[i]
                second_string += '-'
                value += (-sigma)
        elif len(s) == 1:
            first_string, second_string, value = backtrack(score(m, mu, sigma, s, t), m, mu, sigma, s, t)
        else:
            mid = len(s) // 2
            left_columns = score(m, mu, sigma, s[:mid], t)
            right_columns = score(m, mu, sigma, ''.join(list(reversed(s[mid:]))), ''.join(list(reversed(t))))

            mid_column = list(map(lambda x: x[0] + x[1],
                                  zip([r[1] for r in left_columns],
                                      list(reversed([r[1] for r in right_columns])))))

            row_number = mid_column.index(max(mid_column))

            first_string, second_string, value = list(map(lambda x: x[0] + x[1],
                                                          zip(align_recursive(m, mu, sigma, s[0: mid], t[0: row_number]),
                                                              align_recursive(m, mu, sigma, s[mid: ], t[row_number:]))))

        return first_string, second_string, value
    first_string, second_string, value = align_recursive(m, mu, sigma, s, t)
    return '\n'.join([str(value), first_string, second_string])

class TestLinearSpaceAlignment(unittest.TestCase):

    def test_base_case(self):
        assert align(m=1, mu=1, sigma=2, s='GAGA', t='GAT') == '\n'.join([str(-1), 'GAGA', 'GA-T'])

    def test_correct_identification_of_middle_edge(self):
        assert align(m=1, mu=5, sigma=1, s='TT', t='CC') == '\n'.join([str(-4), 'TT--', '--CC'])

    def test_continous_mismatch_when_indel_is_expensive(self):
        assert align(m=1, mu=1, sigma=5, s='TT', t='CC') == '\n'.join([str(-2), 'TT', 'CC'])

    def test_lower_upper_submatrices_are_properly_aligned(self):
        assert align(m=1, mu=5, sigma=1, s='GAACGATTG', t='GGG') == '\n'.join([str(-3), 'GAACGATTG', 'G---G---G'])

    def test_when_match_score_not_equal_to_one(self):
        assert align(m=2, mu=3, sigma=1, s='GCG', t='CT') == '\n'.join([str(-1), 'GCG-', '-C-T'])

    def test_when_second_string_is_one_character_log(self):
        assert align(m=1, mu=2, sigma=3, s='ACAGCTA', t='G') == '\n'.join([str(-17), 'ACAGCTA', '---G---'])

    def test_when_first_string_is_one_character_long(self):
        assert align(m=3, mu=4, sigma=1, s='A', t='CGGAGTGCC') == '\n'.join([str(-5), '---A-----', 'CGGAGTGCC'])

    # Example can be found here - https://en.wikipedia.org/wiki/Hirschberg%27s_algorithm
    def test_wikipedia_example(self):
        assert align(m=2, mu=1, sigma=2, s='AGTACGCA', t='TATGC') == '\n'.join([str(1), 'AGTACGCA', '--TATGC-'])

unittest.main(argv=[''], verbosity=2, exit=False)