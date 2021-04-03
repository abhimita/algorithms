#!/usr/bin/env python

import unittest

# Find a highest-scoring global alignment between two strings (with affine gap penalties).
# Input: A match score m, a mismatch penalty μ, a gap opening penalty σ, a gap extension penalty ε,
# and two DNA strings s and t.
# Output: The maximum alignment score of an alignment between s and t (using affine gap penalties)
# followed by an alignment achieving this maximum score.
# A gap is a contiguous sequence of spaces in a row of an alignment. One way to score gaps more
# appropriately is to define an affine penalty for a gap of length k as σ + ε · (k − 1), where σ is
# the gap opening penalty, assessed to the first symbol in the gap, and ε is the gap extension penalty,
# assessed to each additional symbol in the gap. We typically select ε to be smaller than σ so that
# the affine penalty for a gap of length k is smaller than the penalty for k independent
# single-nucleotide indels (σ · k).

# Input Format. The first line of the input contains m followed by μ followed by σ followed by ε
# (separated by spaces), the second line of the input contains a DNA string s, and the third line
# of the input contains a DNA string t.
# Output Format. The first line of the output should contain the maximum score of an alignment between
# s and t using affine gap penalties, and the next two lines should contain an alignment achieving
# this maximum score. Specifically, the second line should contain s with gaps placed appropriately,
# and the third line should contain t with gaps placed appropriately.

def print_cost_matrix(dp, var=''):
    print(var)
    print('*' * 10)
    for i in range(0, len(dp)):
        for j in range(0, len(dp[i])):
            print(dp[i][j], end=',')
        print()
    print('*' * 10)

def backtrack(i, j, k, s, t, M_X_Y, m, mu, eps, sigma):
    for n in range(0, 3):
        if k == 0 and i - 1 >= 0 and j - 1 >= 0:
            expected_value = M_X_Y[n][i - 1][j - 1] + (m if s[j -1] == t[i -1] else -mu)
            if expected_value == M_X_Y[k][i][j]:
                return i - 1, j - 1, n, s[j - 1], t[i - 1]
        elif k == 1 and j - 1 >= 0:
            expected_value = M_X_Y[n][i][j - 1] - (eps if n == k else sigma)
            if expected_value == M_X_Y[k][i][j]:
                return i, j - 1, n, s[j - 1], '-'
        else:
            expected_value = M_X_Y[n][i - 1][j] - (eps if n == k else sigma)
            if expected_value == M_X_Y[k][i][j]:
                return i - 1, j, n, '-', t[i - 1]

def compose(M, X, Y, s, t, m, mu, sigma, eps):
    aligned_s = []
    aligned_t = []
    i = len(t)
    j = len(s)

    M_X_Y = {0: M, 1: X, 2: Y}

    k = 0
    max_score = M_X_Y[k][i][j]
    for n in range(0, 3):
        if M_X_Y[n][i][j] >= max_score:
            max_score = M_X_Y[n][i][j]
            k = n

    while i > 0 or j > 0:
        i, j, k, s_char, t_char = backtrack(i, j, k, s, t, M_X_Y, m, mu, eps, sigma)
        aligned_s.append(s_char)
        aligned_t.append(t_char)

    return ''.join(reversed(aligned_s)) + '\n' + ''.join(reversed(aligned_t))


def align(m, mu, sigma, eps, s, t):
    row = [float('-inf') for _ in range(len(s) + 1)]
    Y = [row[0:] for _ in range(len(t) + 1)]
    Y[0][0] = 0
    for i in range(1, len(t) + 1):
        Y[i][0] = Y[i - 1][0] - (eps if i > 1 else sigma)

    X = [row[0:] for _ in range(len(t) + 1)]
    X[0][0] = 0
    for j in range(1, len(s) + 1):
        X[0][j] = X[0][j - 1] - (eps if j > 1 else sigma)
    M = [row[0:] for _ in range(len(t) + 1)]
    M[0][0] = 0

    for i in range(1, len(t) + 1):
        for j in range(1, len(s) + 1):
            M[i][j] = max(X[i - 1][j - 1],
                          Y[i - 1][j - 1],
                          M[i - 1][j - 1]) + (m if s[j - 1] == t[i - 1] else -mu)
            X[i][j] = max(X[i][j - 1] - eps,
                          M[i][j - 1] - sigma,
                          Y[i][j - 1] - sigma)
            Y[i][j] = max(Y[i - 1][j] - eps,
                          M[i - 1][j] - sigma,
                          X[i - 1][j] - sigma)

    # aligned_s, aligned_t = compose(M, X, Y, s, t)
    result = str(max(M[len(t)][len(s)],
                     X[len(t)][len(s)],
                     Y[len(t)][len(s)])) + '\n' +     compose(M, X, Y, s, t, m, mu, sigma, eps)

    return result

class TestAffineGapPenalties(unittest.TestCase):


    def test_base_case(self):
        assert align(m=1, mu=3, sigma=2, eps=1, s='GA', t='GTTA') == '-1\nG--A\nGTTA'

    def test_parsing_gap_opening_extension_penalities(self):
        assert align(m=1, mu=5, sigma=3, eps=1, s='TTT', t='TT') == '-1\nTTT\nTT-'

    def test_initialization_of_lower_uper_matrix(self):
        assert align(m=1, mu=5, sigma=2, eps=1, s='CCAT', t='GAT') == '-3\n-CCAT\nG--AT'

    def test_gap_extension_penalty_is_not_equal_to_one(self):
        assert align(m=1, mu=2, sigma=3, eps=2, s='CAGGT', t='TAC') == '-8\nCAGGT\nTAC--'

    def test_when_two_strings_are_of_same_length(self):
        assert align(m=2, mu=3, sigma=3, eps=2, s='GTTCCAGGTA', t='CAGTAGTCGT') == '-8\n--GT--TCCAGGTA\nCAGTAGTC---GT-'

    def test_when_first_string_is_longer_than_second(self):
        assert align(m=1, mu=3, sigma=1, eps=1, s='AGCTAGCCTAG', t='GT') == '-7\nAGCTAGCCTAG\n-----G--T--'

    def test_when_second_string_is_longer_than_first(self):
        assert align(m=2, mu=1, sigma=2, eps=1, s='AA', t='CAGTGTCAGTA') == '-7\n-------A--A\nCAGTGTCAGTA'

    def test_usage_of_all_three_different_matrices(self):
        assert align(m=5, mu=2, sigma=15, eps=5, s='ACGTA', t='ACT') == '-12\nACGTA\nACT--'

unittest.main(argv=[''], verbosity=2, exit=False)
