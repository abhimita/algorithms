#python3
import sys
import unittest

# Find a highest-scoring fitting alignment between two strings.
# Input: A match score m, a mismatch penalty μ, a gap penalty σ, and two DNA strings s and t.
# Output: The maximum alignment score of a fitting alignment between s and t followed by a
# fitting alignment achieving this maximum score.
# We wish to compare the approximately 60,000 nucleotide-long antibiotics-producing gene (NRP synthetase)
# from Bacillus brevis with the approximately 1,800 nucleotide-long segment of an antibiotics-producing
# gene (A-domain) from Streptomyces roseosporus, the bacterium that produces the powerful antibiotic
# daptomycin. We hope to find a region within the longer sequence s that has high similarity with ALL
# of the shorter sequence t. Global alignment will not work because it tries to align all of s to
# all of t; local alignment will not work because it tries to align substrings of both s and t.
# Thus, we have a distinct application called the Fitting Alignment Problem. “Fitting” t to s
# requires finding a substring s’ of s that maximizes the global alignment score between s’ and t
# among all substrings of s.

# Input Format. The first line of the input contains m followed by μ followed by σ (separated by spaces),
# the second line of the input contains a string s, and the third line of the input contains a string t.
# Output Format. The first line of the output should contain the score of an optimal fitting alignment
# between s and t, and the next two lines should contain a fitting alignment achieving this maximum
# score. Specifically, the second line should contain a substring of s with gaps placed appropriately,
# and the third line should contain t with gaps placed appropriately.

def print_cost_matrix(fcs):
    for i in range(0, len(fcs)):
        for j in range(0, len(fcs[i])):
            print(fcs[i][j], end=' ')
        print()

def align(m, mu, sigma, s, t):
    row = [(0, 0) for _ in range(len(s) + 1)]
    fcs = [row[0:] for _ in range(len(t) + 1)]
    for j in range(1, len(s) + 1):
        fcs[0][j] = (0, 0)
    for i in range(1, len(t) + 1):
        fcs[i][0] = (fcs[i - 1][0][0] - sigma, (i - 1) * (len(s) + 1) + 0)

    max_j = -1
    last_row_max_value = float('-inf')
    for i in range(1, len(t) + 1):
        for j in range(1, len(s) + 1):
            fcs[i][j] = (max(fcs[i - 1][j][0] - sigma,
                             fcs[i][j - 1][0] - sigma,
                             fcs[i - 1][j - 1][0] + (m if s[j - 1] == t[i - 1] else -mu)
                            ), None)
            if fcs[i][j][0] == fcs[i - 1][j - 1][0] + (m if s[j - 1] == t[i - 1] else -mu):
                fcs[i][j] = (fcs[i][j][0], (i - 1) * (len(s) + 1) + j - 1)
            elif fcs[i][j][0] == fcs[i][j - 1][0] - sigma:
                fcs[i][j] = (fcs[i][j][0], i * (len(s) + 1) + j - 1)
            elif fcs[i][j][0] == fcs[i - 1][j][0] - sigma:
                fcs[i][j] = (fcs[i][j][0], (i - 1) * (len(s) + 1) + j)

            if i == len(t) and fcs[i][j][0] >= last_row_max_value:
                last_row_max_value = fcs[i][j][0]
                max_j = j

    i = len(t)
    j = max_j
    path = [i * (len(s) + 1) + j]
    while i > 0 and j > 0:
        path.append(fcs[i][j][1])
        i, j = fcs[i][j][1] // (len(s) + 1), fcs[i][j][1] % (len(s) + 1)
    first_string = []
    second_string = []
    path.reverse()

    for index, p in enumerate(path):
        i, j = p // (len(s) + 1), p % (len(s) + 1)
        if (i, j) == (0,0): continue
        prev_i, prev_j = path[index - 1] // (len(s) + 1), path[index - 1] % (len(s) + 1)
        if i - prev_i == 1 and j - prev_j == 1:
            if fcs[i][j][0] != fcs[prev_i][prev_j][0]:
                second_string.append(t[prev_i])
                first_string.append(s[prev_j])
        elif i - prev_i == 0 and j - prev_j == 1:
            second_string.append('-')
            first_string.append(s[prev_j])
        elif i - prev_i == 1 and j - prev_j == 0:
            second_string.append(t[prev_i])
            first_string.append('-')
    return str(fcs[len(t)][max_j][0]) + '\n' + ''.join(first_string) + '\n' + ''.join(second_string)

class TestFittingAligment(unittest.TestCase):
    def test_base_case(self):
        assert align(m=1, mu=1, sigma=2, s='GAGA', t='GAT') == '1\nGAG\nGAT'

    def test_no_penalty_for_starting_at_arbitrary_position_and_indel_outside_second_str(self):
        assert align(m=1, mu=1, sigma=1, s='CCAT', t='AT') == '2\nAT\nAT'

    def test_global_or_local_alignment_is_not_used(self):
        assert align(m=1, mu=5, sigma=1, s='CACGTC', t='AT') == '0\nACGT\nA--T'

    def test_correct_cell_of_dp_matrix_is_chosen(self):
        assert align(m=1, mu=1, sigma=1, s='ATCC', t='AT') == '2\nAT\nAT'

    def test_input_strings_of_same_size(self):
        assert align(m=2, mu=3, sigma=1, s='ACGACAGAG', t='CGAGAGGTT') == '7\nCGA-CAGAG--\nCGAG-AG-GTT'

unittest.main(argv=[''], verbosity=2, exit=False)