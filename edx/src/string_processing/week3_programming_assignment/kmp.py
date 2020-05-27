# python3
import unittest
import numpy as np
import regex as re

# Longest common prefix
def generate_lcp(text):
    lcp = [0] * len(text)
    lcp[0] = 0
    i = 1
    j = 0
    while i < len(text):
        if text[i] == text[j]:
            lcp[i] = j + 1
            i += 1
            j += 1
        else:
            if j == 0:
                lcp[i] = 0
                i += 1
            else:
                j = lcp[j - 1]
    return lcp

# Knuth-Morris-Pratt algorithm
def find_pattern(pattern, text):
    new_string = pattern + '$' + text
    lcp = generate_lcp(new_string)
    pattern_length = len(pattern)
    results = []
    for i in range(pattern_length + 1, len(new_string)):
        if lcp[i] == pattern_length:
            results.append(i - 2 * pattern_length)
    return results

def find_pattern_naive(pattern, text):
    results = []
    for i in range(len(text) - len(pattern) + 1):
        found = True
        for j in range(len(pattern)):
            if pattern[j] != text[i + j]:
                found = False
                break
        if found:
            results.append(i)
    return results

def build_suffix_array(text):
    suffix_array = []
    def sort(text, positions=range(0, len(text)), step=1):
        bucket = {}
        for i in positions:
            key = text[i:i + step]
            if bucket.get(key, '') == '':
                bucket[key] = [i]
            else:
                bucket[key].append(i)
        for k in sorted(bucket.items(), key=lambda x: x[0]):
            if len(k[1]) == 1:
                suffix_array.append(k[1][0])
            else:
                sort(text, k[1], 2*step)
    sort(text)
    return suffix_array

# Finds all occurrences using suffix array
# First build the suffix array and then do binary search
def find_all_matches_using_sa(text, pattern):
    def first(sa, text, pattern, low, high):
        if low > high:
            return -1
        else:
            mid = (low + high) // 2
            if text[sa[mid]: sa[mid] + len(pattern)] == pattern and (mid == 0 or text[sa[mid - 1]:sa[mid - 1] + len(pattern)] < pattern):
                return mid
            elif text[sa[mid]: sa[mid] + len(pattern)] < pattern:
                return first(sa, text, pattern, mid + 1, high)
            else:
                return first(sa, text, pattern, low, mid - 1)

    def last(sa, text, pattern, low, high):
        if low > high:
            return -1
        else:
            mid = (low + high) // 2
            if text[sa[mid]: sa[mid] + len(pattern)] == pattern and (mid == len(sa) - 1 or text[sa[mid + 1]:sa[mid + 1] + len(pattern)] > pattern):
                return mid
            elif text[sa[mid]: sa[mid] + len(pattern)] > pattern:
                return last(sa, text, pattern, low, mid - 1)
            else:
                return last(sa, text, pattern, mid + 1, high)

    def search(sa, text, pattern, low, high):
        start = first(sa, text, pattern, low, high)
        if start == -1:
            return -1, -1
        end = last(sa, text, pattern, start + 1, high)
        return start, end
    sa = build_suffix_array(text)
    start, end = search(sa, text, pattern, 0, len(sa) - 1)
    if end == -1:
        end = start + 1
    else:
        end += 1
    results = []
    if start != -1:
        for i in range(start, end):
            results.append(sa[i])
    return results

def find_all_using_re(text, pattern):
    return [m.start() for m in re.finditer(pattern, text, overlapped=True)]

class TestKMP(unittest.TestCase):
    def test_pattern_with_no_occurrence(self):
        pattern = 'GT'
        text = 'TACG'
        actual = find_pattern(pattern, text)
        expected = find_pattern_naive(pattern, text)
        assert actual == expected

    def test_pattern_with_two_overlapping_occurrences(self):
        pattern = 'ATA'
        text = 'ATATA'
        actual = find_pattern(pattern, text)
        expected = find_pattern_naive(pattern, text)
        assert actual == expected

    def test_pattern_more_than_two_occurrences(self):
        pattern = 'ATAT'
        text = 'GATATATGCATATACTT'
        actual = find_pattern(pattern, text)
        expected = find_pattern_naive(pattern, text)
        assert actual == expected

    def test_pattern_repeated_at_every_position(self):
        pattern = 'A'
        text = 'AAA'
        actual = find_pattern(pattern, text)
        expected = find_pattern_naive(pattern, text)
        assert actual == expected

    def test_for_all_distinct_characters_and_no_match(self):
        text = "TACG" + '$'
        pattern = 'GT'
        expected = []
        assert find_all_matches_using_sa(text, pattern) == expected
        assert find_pattern(text, pattern) == expected

    def test_for_3_occurrences(self):
        text = 'GATATATGCATATACTT$'
        pattern = 'ATAT'
        expected = [1, 3, 9]
        assert sorted(find_all_matches_using_sa(text, pattern)) == expected
        assert find_pattern(pattern, text[:-1]) == expected

    def test_for_50_char_randomly_generated_string(self):
        text = ''.join(np.random.choice(['A', 'C', 'T', 'G'], 50)) + '$'
        pattern = 'AT'
        expected = find_all_using_re(text, pattern)
        match_using_sa = sorted(find_all_matches_using_sa(text, pattern))
        match_using_kmp = find_pattern(pattern, text[:-1])
        assert match_using_sa == expected
        assert match_using_kmp == expected

    def test_for_5000000_char_randomly_generated_string(self):
        text = ''.join(np.random.choice(['A', 'C', 'T', 'G'], 5000000)) + '$'
        pattern = 'ATAT'
        expected = find_all_using_re(text, pattern)
        assert sorted(find_all_matches_using_sa(text, pattern)) == expected
        assert find_pattern(pattern, text[:-1]) == expected

    def test_10000_times_for_500_char_randomly_generated_string(self):
        for i in range(10000):
            text = ''.join(np.random.choice(['A', 'C', 'T', 'G'], 500)) + '$'
            pattern = 'ATAT'
            expected = find_all_using_re(text, pattern)
            assert sorted(find_all_matches_using_sa(text, pattern)) == expected
            assert find_pattern(pattern, text[:-1]) == expected

if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)

