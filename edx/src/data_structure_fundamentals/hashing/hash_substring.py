import random
import unittest

def string_match_brute_force(text, word):
    m = len(text)
    n = len(word)
    match_position = []
    if m < n:
        return match_position
    for i in range(0, m - n + 1):
        if word == text[i : i + n]:
            match_position.append(i)
    return(match_position)

# Implements Rabin Karp algorithm with rolling hash
# Polynomial hash function allows us to compute subsequent hash value from previous one
# Modulo operation takes care of the resulting value not encountering overflow
# That also means collisions can happen. So even after hash(a) = hash(b) we need to check a == b
# Few modulo rules to keep in mind are:
# a % b = ( a + b) % b - we may need to do this if 'a' becomes negative
# (a + b ) % c = ((a % c) + (b % c)) % c
# (a * b) % c = ((a %c) * (b % c)) %c
def rolling_hash(text, pattern):
    p_len = len(pattern)
    t_len = len(text)
    multiplier = 263
    prime = 100000007
    match = []

    if p_len > t_len:
        return match

    text_hash = pattern_hash = 0
    for i in range(p_len):
        text_hash = (text_hash * multiplier + ord(text[i])) % prime
        pattern_hash = (pattern_hash * multiplier + ord(pattern[i])) % prime

    # Important not to use math.pow as it uses floating point arithmetic
    m = pow(multiplier, p_len - 1) % prime

    for index, i in enumerate(range(t_len - p_len + 1)):
        if index > 0:
            text_hash = (text_hash - ord(text[index - 1]) * m) % prime
            text_hash = (text_hash * multiplier + ord(text[p_len + index - 1])) % prime
            text_hash = (text_hash + prime) % prime

        if text_hash == pattern_hash:
            if pattern == text[index: index + p_len]:
                match.append(i)
    return(match)

class TestRollingHash(unittest.TestCase):
    def test_large_pattern_to_check_for_overflow(self):
        text = 'eaabcdbecceacbeacbcabbbbecbcceddcedadadcabcbcecdcbdedbedcdeabcbeccaeeceadaebbcaecbeacdedcceabbddecae'
        word = 'beacbcabbbbecbcceddcedadadcab'
        self.assertEqual(rolling_hash(text, word), string_match_brute_force(text,word))

    def test_find_match_for_multiple_match_at_start_and_end(self):
        text = 'abacaba'
        word = 'aba'
        self.assertEqual(rolling_hash(text, word), string_match_brute_force(text,word))

    def test_find_match_for_multiple_match_at_every_position_after_first(self):
        text = 'baaaaaaa'
        word = 'aaaaa'
        self.assertEqual(rolling_hash(text, word), string_match_brute_force(text,word))

    def test_find_match_when_word_longer_than_text(self):
        text = 'baaaaaaa'
        word = 'aaaaaxtyrwpd'
        self.assertEqual(rolling_hash(text, word), string_match_brute_force(text,word))

    def test_find_match_when_text_is_empty(self):
        text = ''
        word = 'aaaaaxtyrwpd'
        self.assertEqual(rolling_hash(text, word), string_match_brute_force(text, word))

    def test_find_match_when_pattern_is_empty(self):
        text = 'abcd'
        word = ''
        self.assertEqual(rolling_hash(text, word), string_match_brute_force(text, word))


unittest.main(argv=[''], verbosity=2, exit=False)
