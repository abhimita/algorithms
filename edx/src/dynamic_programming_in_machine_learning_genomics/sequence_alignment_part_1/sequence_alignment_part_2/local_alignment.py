#python3
import sys
import unittest
import pprint as pp

def print_lcs(lcs):
    for i in range(0, len(lcs)):
        for j in range(0, len(lcs[i])):
            print(lcs[i][j], end=' ')
        print()

def align(m, mu, sigma,s,t):
    row = [(0, 0) for _ in range(len(s) + 1)]
    lcs = [row[0:] for _ in range(len(t) + 1)]
    max_i = -1
    max_j = -1
    max_value = float('-inf')
    for j in range(1, len(s) + 1):
        lcs[0][j] = (0, 0)
    for i in range(1, len(t) + 1):
        lcs[i][0] = (0, 0)

    for i in range(1, len(t) + 1):
        for j in range(1, len(s) + 1):
            lcs[i][j] = (max(lcs[0][0][0] ,
                             lcs[i - 1][j - 1][0] + (m if s[j -1] == t[i - 1] else -mu),
                             lcs[i - 1][j][0] - sigma,
                             lcs[i][j - 1][0] - sigma), None)
            if lcs[i][j][0] == 0:
                lcs[i][j] = (lcs[i][j][0], 0)
            elif lcs[i][j][0] == lcs[i - 1][j - 1][0] + (m if s[j -1] == t[i - 1] else -mu):
                lcs[i][j] = (lcs[i][j][0], (i  - 1) * (len(s) + 1) + j - 1)
            elif lcs[i][j][0] == lcs[i - 1][j][0] - sigma:
                lcs[i][j] = (lcs[i][j][0], (i  - 1) * (len(s) + 1) + j)
            else:
                lcs[i][j] = (lcs[i][j][0], i * (len(s) + 1) + j - 1)

            if i == len(t) and j == len(s):
                lcs[i][j] = (max(max_value, lcs[i][j][0]),
                             max_i * (len(s) + 1) + max_j if max(max_value, lcs[i][j][0]) == max_value else lcs[i][j][1])
            else:
                if lcs[i][j][0] > max_value:
                    max_value = lcs[i][j][0]
                    max_i = i
                    max_j = j

    i = len(t)
    j = len(s)
    path = [i * (len(s) + 1) + j]
    while i > 0 and j > 0 and lcs[i][j][0] != 0:
        path.append(lcs[i][j][1])
        i, j = lcs[i][j][1] // (len(s) + 1), lcs[i][j][1] % (len(s) + 1)
    first_string = []
    second_string = []
    path.reverse()
    for index, p in enumerate(path):
        i, j = p // (len(s) + 1), p % (len(s) + 1)
        if (i, j) == (0,0): continue
        prev_i, prev_j = path[index - 1] // (len(s) + 1), path[index - 1] % (len(s) + 1)
        if i - prev_i == 1 and j - prev_j == 1:
            if lcs[i][j][0] != lcs[prev_i][prev_j][0]:
                second_string.append(t[prev_i])
                first_string.append(s[prev_j])
        elif i - prev_i == 0 and j - prev_j == 1:
            second_string.append('-')
            first_string.append(s[prev_j])
        elif i - prev_i == 1 and j - prev_j == 0:
            second_string.append(t[prev_i])
            first_string.append('-')
    return str(lcs[len(t)][len(s)][0]) + '\n' + ''.join(first_string) + '\n' + ''.join(second_string)

class TestLocalAlignment(unittest.TestCase):
    def test_base_case(self):
        assert align(m=1, mu=1, sigma=2, s='GAGA', t='GAT') == '2\nGA\nGA'

    def test_for_correct_first_line_parsing(self):
        assert align(m=3, mu=3, sigma=1, s='AGC', t='ATC') == '4\nAG-C\nA-TC'

    def test_for_penalities_are_subtracted_correctly(self):
        assert align(m=1, mu=1, sigma=1, s='AT', t='AG') == '1\nA\nA'

    def test_reconstruction_using_free_ride(self):
        assert align(m=1, mu=1, sigma=1, s='TAACG', t='ACGTG') == '3\nACG\nACG'

    def test_when_first_string_is_larger_than_second_string(self):
        assert align(m=3, mu=2, sigma=1, s='CAGAGATGGCCG', t='ACG') == '6\nCG\nCG'

    def test_when_second_string_is_larger_than_first_string(self):
        assert align(m=2, mu=3, sigma=1, s='CTT', t='AGCATAAAGCATT') == '5\nC-TT\nCATT'

unittest.main(argv=[''], verbosity=2, exit=False)