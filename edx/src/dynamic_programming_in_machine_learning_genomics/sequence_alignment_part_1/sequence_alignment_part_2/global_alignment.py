import unittest
import unittest
# Find a highest-scoring alignment between two strings.
# Input: A match score m, a mismatch penalty μ, a gap penalty σ, and two DNA strings s and t.
# Output: The maximum alignment score of s and t followed by an alignment achieving this maximum score.
# You are a Bioinformatician and you have obtained two gene sequences, s and t. You want to line up the
# two sequences to find positions at which they are the same, which could imply some evolutionary
# relationship. The score of an alignment is defined as the sum of the scores of each position of the
# alignment, the score of a match is +m, the score of a mismatch is -μ, and the score of a gap is -σ.
# Below is an example of scoring an alignment between the sequences ATGTTATA and ATCGTCC using a
# match score of m = 1, a mismatch penalty of μ = 1, and a gap penalty of σ = 2.

# Input Format. The first line of the input contains m followed by μ followed by σ (separated by spaces),
# the second line of the input contains a DNA string s, and the third line of the input contains a DNA
# string t.

# Output Format. The first line of the output should contain the maximum score of an alignment between s
# and t, and the next two lines should contain an alignment achieving this maximum score. Specifically,
# the second line should contain s with gaps placed appropriately, and the third line should contain t
# with gaps placed appropriately.

def align(m, mu, sigma, s, t):
    column = [0 for _ in range(0, len(s) + 1)]
    lcs = [column[0:] for _ in range(0, len(t) + 1)]
    for j in range(1, len(s) + 1):
        lcs[0][j] = lcs[0][j - 1] + -1 * sigma
    for i in range(1, len(t) + 1):
        lcs[i][0] = lcs[i - 1][0] + -1 * sigma
    for i in range(1, len(t) + 1):
        for j in range(1, len(s) + 1):
            if s[j - 1] == t[i - 1]:
                lcs[i][j] = lcs[i - 1][j - 1] + m
            else:
                lcs[i][j] = max(lcs[i -1][j - 1] - mu, lcs[i - 1][j] - sigma, lcs[i][j - 1] - sigma)
    i = len(t)
    j = len(s)
    first_str = []
    second_str = []
    while i > 0 and j > 0:
        max_value = max(lcs[i - 1][j - 1] - mu, lcs[i - 1][j] - sigma, lcs[i][j - 1] - sigma)
        if s[j - 1] == t[i - 1] or max_value == lcs[i - 1][j - 1] - mu:
            first_str.append(s[j - 1])
            second_str.append(t[i - 1])
            i -= 1
            j -= 1
        elif lcs[i - 1][j] - sigma == max_value:
            first_str.append('-')
            second_str.append(t[i - 1])
            i -= 1
        else:
            first_str.append(s[j - 1])
            second_str.append('-')
            j -= 1
    while j > 0:
        first_str.append(s[j - 1])
        second_str.append('-')
        j -= 1
    while i > 0:
        first_str.append('-')
        second_str.append(t[i - 1])
        i -= 1
    return str(lcs[len(t)][len(s)]) + '\n' + \
           ''.join(reversed(first_str)) + '\n' + \
           ''.join(reversed(second_str))

class TestAligment(unittest.TestCase):

    def test_base_case(self):
        assert align(m=1, mu=1, sigma=2, s='GAGA', t='GAT') == '-1\nGAGA\nGA-T'

    def test_correct_penalites_are_applied(self):
        assert align(m=1, mu=3, sigma=1, s='ACG', t='ACT') == '0\nACG-\nAC-T'

    def test_penalty_is_subtracted(self):
        assert align(m=1, mu=1, sigma=1, s='AT', t='AG') == '0\nAT\nAG'

    def test_first_transformation_is_indel(self):
        assert align(m=2, mu=5, sigma=1, s='TCA', t='CA') == '3\nTCA\n-CA'

    def test_multiple_indels_are_handled(self):
        assert align(m=1, mu=10, sigma=1, s='TTTTCCTT', t='CC') == '-4\nTTTTCCTT\n----CC--'

    def test_when_second_string_is_shorter_than_first(self):
        assert align(m=2, mu=3, sigma=2, s='ACAGATTAG', t='T') == '-14\nACAGATTAG\n------T--'

    def test_when_second_string_is_longer_than_first(self):
        assert align(m=3, mu=1, sigma=2, s='G', t='ACATACGATG') == '-15\n---------G\nACATACGATG'

unittest.main(argv=[''], verbosity=2, exit=False)