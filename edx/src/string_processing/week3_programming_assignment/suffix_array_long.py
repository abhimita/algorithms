import sys
import unittest
import numpy as np

# Ref: very good reference of step-by-step construction of suffix array with O(nlogn) complexity
# https://cp-algorithms.com/string/suffix-array.html#toc-tgt-3
# sa -> suffix array
# equiv -> equivalence class
alphabet = {'$': 0, 'A': 1, 'C' : 2, 'G' : 3, 'T': 4}

def build_suffix_array_naive(text):
    sa = []
    for i in range(0, len(text)):
        sa.append((i, text[i:] + text[0:i]))
    result = [y[0] for y in sorted(sa, key=lambda x: x[1])]
    return result


def counting_sort(text):
    n = len(text)
    count = [0] * len(alphabet)
    sa = [0] * n
    equiv = [0] * n
    for t in text:
        count[alphabet[t]] += 1
    for i in range(1, len(count)):
        count[i] += count[i - 1]
    for i in range(0, n):
        count[alphabet[text[i]]] -= 1
        sa[count[alphabet[text[i]]]] = i
    # build equivalence class
    equiv[sa[0]] = max_equiv = 0
    for i in range(1, len(sa)):
        equiv[sa[i]] = equiv[sa[i - 1]] + (1 if text[sa[i]] != text[sa[i - 1]] else 0)
        if equiv[sa[i]] > max_equiv:
            max_equiv = equiv[sa[i]]
    return sa, equiv, max_equiv

def build_suffix_array(text):
    # Sort by each character
    sa, equiv, max_equiv = counting_sort(text)
    n = len(text)
    h = 0
    sa_2 = [0] * n
    # Now expand the substring to two character length
    while (1 << h) <= n:
        for i in range(0, n):
            sa_2[i] = sa[i] - (1 << h) + (n if (1 << h) > sa[i] else 0)
        count = [0] * (max_equiv + 1)
        for i in range(0, n):
            count[equiv[sa_2[i]]] += 1
        for i in range(1, len(count)):
            count[i] += count[i - 1]
        for i in range(n - 1, -1, -1):
            count[equiv[sa_2[i]]] -= 1
            sa[count[equiv[sa_2[i]]]] = sa_2[i]
        equiv_2 = [0] * n
        equiv_2[sa[0]] = max_equiv = 0
        for i in range(1, n):
            current_tuple = (equiv[sa[i]], equiv[(sa[i] + (1 << h)) % n])
            previous_tuple = (equiv[sa[i - 1]], equiv[(sa[i - 1] + (1 << h)) % n])
            equiv_2[sa[i]] = equiv_2[sa[i - 1]] + (1 if current_tuple != previous_tuple else 0)
            if max_equiv < equiv_2[sa[i]]:
                max_equiv = equiv_2[sa[i]]
        equiv = equiv_2
        h += 1
    return sa

class TestSuffixArray(unittest.TestCase):

    def run_test(self, n):
        text = ''.join(np.random.choice(['A', 'C', 'T', 'G'], n)) + '$'
        actual = build_suffix_array(text)
        expected = build_suffix_array_naive(text)
        assert actual == expected

    def test_suffix_array_for_random_string(self):
        print("Test suffix array for 5 character random string. Repeat test for 1000 times")
        for i in range(1000):
            self.run_test(5)
        print("Test suffix array for 100 character random string. Repeat test for 1000 times")
        for i in range(1000):
            self.run_test(100)

unittest.main(argv=[''], verbosity=2, exit=False)