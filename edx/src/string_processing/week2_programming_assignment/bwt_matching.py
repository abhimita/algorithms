import unittest
import bwt
import numpy as np
import regex as re

def count_overlapping(text, search_for):
    return len(re.findall(search_for, text, overlapped=True))

def bwt_matching_driver(last_column, patterns):
    first_occurrence, fm_index = PreprocessBWT(last_column)
    results = []
    for pattern in patterns:
        results.append(CountOccurrences(pattern, last_column, first_occurrence, fm_index))
    return results

# Ref - http://www.csbio.unc.edu/mcmillan/Comp555S16/Lecture22.pdf
def CountOccurrences(pattern, bwt, first_occurrence, fm_index):
    low = 0
    high = len(fm_index) - 1
    for p in pattern[::-1]:
        if fm_index[low].get(p, '') != '':
            low = first_occurrence[p] + fm_index[low][p]
        else:
            return 0
        if fm_index[high].get(p, '') != '':
            high = first_occurrence[p] + fm_index[high][p]
        else:
            return 0
    return 0 if low > high else high - low

def PreprocessBWT(bwt):
    """
    Preprocess the Burrows-Wheeler Transform bwt of some text
    and compute as a result:
      * first_occurrence - for each character C in bwt, starts[C] is the first position
          of this character in the sorted array of
          all characters of the text.
      * fm_index - for each character C in bwt and each position P in bwt,
          occ_count_before[C][P] is the number of occurrences of character C in bwt
          from position 0 to position P inclusive.
    """
    frequency = dict()
    first_occurrence = {} # keys track of first occurrence of a symbol in first column

    for c in bwt:
        if frequency.get(c, '') == '':
            frequency[c] = 1
        else:
            frequency[c] += 1
    prev_key = ''
    for k in sorted(frequency.keys()):
        if prev_key == '':
            frequency[k] = 0
            first_occurrence[k] = 0
        else:
            occurrence = frequency[k]
            frequency[k] += frequency[prev_key]
            first_occurrence[k] = frequency[k] - occurrence + 1
        prev_key = k
    fm_index = [dict([(k, 0) for k in frequency.keys()]) for i in range(len(bwt) + 1)]
    for i in range(0, len(bwt)):
        for k in frequency.keys():
            fm_index[i + 1][k] = fm_index[i][k] + (1 if k == bwt[i] else 0)
    return first_occurrence, fm_index

class TestBetterBWTMatching(unittest.TestCase):
    def setup(self, text_length, pattern_length):
        text = ''.join(np.random.choice(['A', 'C', 'T', 'G'], 20)) + '$'
        bwt_string = bwt.BWT(text)
        patterns = []
        for i in range(2):
            patterns.append(''.join(np.random.choice(['A', 'C', 'T', 'G'], 3)))
        return text, bwt_string, patterns

    def get_expected_results(self, text, patterns):
        expected = []
        for p in patterns:
            expected.append(len(re.findall(p, text, overlapped=True)))
        return expected

    def test_single_pattern_appearing_more_than_once(self):
        bwt_string = 'AGGGAA$'
        patterns = ['GA']
        actual = bwt_matching_driver(bwt_string, patterns)
        assert actual == [3]

    def test_two_patterns_appearing_more_than_once(self):
        bwt_string = 'ATT$AA'
        patterns = ['ATA', 'A']
        actual = bwt_matching_driver(bwt_string, patterns)
        assert actual == [2, 3]

    def test_two_patterns_both_not_appearing(self):
        bwt_string = 'AT$TCTATG'
        patterns = ['TCT', 'TATG']
        actual = bwt_matching_driver(bwt_string, patterns)
        assert actual == [0, 0]

    def test_with_20_character_random_text_and_two_three_character_patterns_repeat_1000_times(self):
        for j in range(1000):
            text, bwt_string, patterns = self.setup(20, 3)
            actual = bwt_matching_driver(bwt_string, patterns)
            expected = self.get_expected_results(text, patterns)
            assert actual == expected

    def test_with_6000_character_random_text_and_two_three_character_patterns_repeat_1000_times(self):
        for j in range(1000):
            text, bwt_string, patterns = self.setup(60, 3)
            actual = bwt_matching_driver(bwt_string, patterns)
            expected = self.get_expected_results(text, patterns)
            assert actual == expected

if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)