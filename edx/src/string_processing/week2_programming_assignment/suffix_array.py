#!/usr/bin/env python
import unittest
import sys
import numpy as np

def build_suffix_array_naive(text):
    return [len(text) - len(x) for x in sorted([text[i:] for i in range(0, len(text))])]

# Manber Meyers algorithm - ref: https://stackoverflow.com/questions/18495728/suffix-array-using-manber-myers-algorithm
def build_suffix_array_manber_meyers(text):
    suffix_array = []
    def sort(text, start_pos=range(0, len(text)), step=1):
        bucket = {}
        for i in start_pos:
            key = text[i: i + step]
            if bucket.get(key,'') == '':
                bucket[key] = [i]
            else:
                bucket[key].append(i)
        for k in sorted(bucket.items(), key=lambda x: x[0]):
            if len(k[1]) == 1:
                suffix_array.append(k[1][0])
            else:
                sort(text, k[1], step=2*step)
        return suffix_array
    return sort(text)

class TestBuildSuffixArray(unittest.TestCase):
    def test_for_all_distinct_characters(self):
        text = "GCA$"
        assert build_suffix_array_naive(text) == build_suffix_array_manber_meyers(text)

    def test_for_16_character_string(self):
        text = "AACGATAGCGGTAGA$"
        assert build_suffix_array_manber_meyers(text) == [15, 14, 0, 1, 12, 6, 4, 2, 8, 13, 3, 7, 9, 10, 11, 5]

    def test_100_character_random_string(self):
        text = ''.join(np.random.choice(['A', 'C', 'T', 'G'], 100)) + '$'
        assert build_suffix_array_naive(text) == build_suffix_array_manber_meyers(text)

if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)

