#python3
import sys
import unittest

# Find an alignment of three strings.

# Input: Strings r, s, and t.

# Output: The maximum score of a multiple alignment of these three strings, followed by a multiple alignment of the
# three strings achieving this maximum using a scoring function in which the score of an alignment column
# is 1 if all three symbols are identical and 0 otherwise.

# You are a Bioinformatician and you have obtained three DNA sequences. You want to line up the amino acids of
# the three sequences to find positions at which they are similar.  The score of an alignment is defined as
# the sum of the scores of each position of the alignment, where the score of a position i is 1 if all 3
# characters match, otherwise 0.

# Input Format. The first line of the input contains a string r, the second line of the input contains a string s,
# and the third line of the input contains a string t.

# Output Format. The first line of the output should contain the maximum score of an alignment between the
# three input strings, and the next three lines should contain an alignment achieving this maximum score.
# Specifically, the second line should contain r with gaps placed appropriately, the third line should
# contain s with gaps placed appropriately, and the fourth line should contain t with gaps placed appropriately.

# Constraints. |r| ≤ 10; |s| ≤ 10; |t| ≤ 10

def align(r, s, t):
    r_s_t = []
    for k in range(0, len(r) + 1):
        panel = []
        for i in range(0, len(t) + 1):
            row = [0 for j in range(0, len(s) + 1)]
            panel.append(row)
        r_s_t.append(panel)

    r_s_t[0][0][0] = 0

    for k in range(1, len(r) + 1):
        for i in range(1, len(t) + 1):
            for j in range(1, len(s) + 1):
                r_s_t[k][i][j] = max(r_s_t[k -1][i - 1][j - 1] +
                                     (1 if r[k - 1] == t[i - 1] and t[i - 1] == s[j - 1] else 0),
                                     r_s_t[k - 1][i][j - 1],
                                     r_s_t[k -1][i - 1][j],
                                     r_s_t[k][i - 1][j - 1],
                                     r_s_t[k - 1][i][j],
                                     r_s_t[k][i][j - 1],
                                     r_s_t[k][i - 1][j])
    return backtrack(r_s_t, r, s, t)

def backtrack(r_s_t, r, s, t):
    k = len(r)
    i = len(t)
    j = len(s)
    value = r_s_t[k][i][j]
    first_string = []
    second_string = []
    third_string = []

    while i > 0 or j > 0 or k > 0:
        if k > 0 and j > 0 and i > 0 and r[k - 1] == t[i - 1] and t[i - 1] == s[j - 1]:
            first_string.append(r[k - 1])
            second_string.append(t[i - 1])
            third_string.append(s[j - 1])
            i = i - 1
            j = j - 1
            k = k - 1
        else:
            max_value = [r_s_t[k - 1][i][j - 1] if k > 0 and j > 0 else float('-inf'),
                         r_s_t[k -1][i - 1][j] if k > 0 and i > 0 else float('-inf'),
                         r_s_t[k][i - 1][j - 1] if i > 0 and j > 0 else float('-inf'),
                         r_s_t[k - 1][i][j] if k > 0 else float('-inf'),
                         r_s_t[k][i][j - 1] if j > 0 else float('-inf'),
                         r_s_t[k][i - 1][j] if i > 0 else float('-inf')]
            index = max_value.index(max(max_value))
            if index == 0:
                first_string.append(r[k - 1])
                second_string.append('-')
                third_string.append(s[j - 1])
                k = k - 1
                j = j - 1
            elif index == 1:
                first_string.append(r[k - 1])
                second_string.append(t[i - 1])
                third_string.append('-')
                k = k - 1
                i = i - 1
            elif index == 2:
                first_string.append('-')
                second_string.append(t[i - 1])
                third_string.append(s[j - 1])
                i = i - 1
                j = j - 1
            elif index == 3:
                first_string.append(r[k - 1])
                second_string.append('-')
                third_string.append('-')
                k = k - 1
            elif index == 4:
                first_string.append('-')
                second_string.append('-')
                third_string.append(s[j - 1])
                j = j - 1
            else:
                first_string.append('-')
                second_string.append(t[i - 1])
                third_string.append('-')
                i = i - 1

    return '\n'.join([str(value),
                      ''.join(reversed(first_string)),
                      ''.join(reversed(third_string)),
                      ''.join(reversed(second_string))])


class TestMultipleAlignment(unittest.TestCase):

    def test_base_case(self):
        assert align(r='ATATCGG', s='TCCGA', t='ATGTACTG') == '\n'.join([str(3), 'AT-ATC-GG', '-T---CCGA', 'ATGTACTG-'])

    def test_scoring_scheme(self):
         assert align(r='A', s='AT', t='A') == '\n'.join([str(1), 'A-', 'AT', 'A-'])

    def test_when_one_of_the_strings_is_primarily_indels(self):
        assert align(r='AAAAT', s='CCCCT', t='T') == '\n'.join([str(1), 'AAAAT', 'CCCCT', '----T'])

    def test_where_first_and_last_character_need_to_be_aligned(self):
        assert align(r='AT', s='ACCT', t='AGGGGT') == '\n'.join([str(2), 'A----T', 'A--CCT', 'AGGGGT'])

    def test_output_zero_when_there_is_no_shared_character(self):
        assert align(r='GGAG', s='TT', t='CCCC') == '\n'.join([str(0), '--GGAG', '----TT', 'CCCC--'])

    def test_three_strings_one_character_long(self):
        assert align(r='T', s='T', t='T') == '\n'.join([str(1), 'T', 'T', 'T'])

unittest.main(argv=[''], verbosity=2, exit=False)
