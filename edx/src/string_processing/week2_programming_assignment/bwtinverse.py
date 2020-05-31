import unittest
import random

# Getting back the original string from the transformed copy
# This is the naive method which requires generating MxM matrix
# where M = length of the string
def InverseBWTNaive(bwt):
    # Take the last column.
    last_column = bwt
    # Sort last column and concatenate as L + F
    # where L -> last and F - > first
    # L is added before since L must have preceded F
    # as we go through the circular rotation
    # Sort the concatenated string that will now form the first two columns
    # Append bwt string as new column to the left of the concatenation
    # Repeat this process
    for i in range(0, len(bwt) - 1):
        last_column = sorted([x[0] + x[1] for x in zip(bwt, sorted(last_column))])
    return last_column[0][1:] + last_column[0][0]

# Memory efficient way to perform BWT reverse transformation
# This relies on last column only
def InverseBWT(bwt):
    rank = [0] * len(bwt)
    total = {}
    runs = {}
    # from the given bwt string find rank of each character
    # while doing that we also count total occurrences of each character
    # This is used later to prepare run length for the first length
    # This run length helps us to find the i-th occurrence of character:x
    # in first column
    for i, c in enumerate(bwt):
        if total.get(c, '') == '':
            total[c] = 0
        else:
            total[c] = total[c] + 1
        rank[i] = total[c]
    # Run length of characters in first column
    nrows = 0
    for k, v in sorted(total.items()):
        runs[k] = (nrows, v)
        nrows += (v + 1)

    # Actual reverse transformation happens here
    r = 0
    # Start from the first character in BWT string
    # This is the last column of BWT matrix
    c = bwt[r]
    # Initialize list with space character
    # We don't do string concatenation at every stage
    # in iteration, as that makes the algorithm slower
    str = [''] * len(bwt)
    pos = len(bwt) - 2
    while c != '$':
        # Add this character to the final string
        # Move in backward to direction to construct the original string
        str[pos] = c
        pos -= 1
        # rank[r] - > get rank of character
        # Recall we started with r = 0
        # We need to move to the first column to find the row
        # where we have r-th occurrence of character c
        # That is computed by adding rank of c as obtained from rank[r]
        # with the starting position of character:c in first column
        # Recall characters in first column are sorted
        r = runs[c][0] + rank[r]
        # We come back and pick up character in the
        # last column with same row number: r
        c = bwt[r]
    # Append the $ at the end
    str[len(bwt) - 1] = '$'
    return ''.join(str)

# The following is a naive algorithm for BWT
# It requires storing of MxM matrix.
# Time complexity is n^3*log(n) because it involves a sort with complexity O(nlogn)
# Comparison involving n character long string is O(n)
# So the total complexity in n^3*logn
def BWT(str):
    str_matrix = []
    for i in range(0, len(str)):
        text = str if i == 0 else str_matrix[i - 1]
        str_matrix.append(text[len(str) - 1:] + text[0: len(str) - 1])
    return ''.join([x[len(str) - 1] for x in sorted(str_matrix)])

class TestBWTInverse(unittest.TestCase):
    def test_bwt_inverse_for_short_string(self):
        bwt = 'AGGGAA$'
        assert InverseBWT(bwt) == InverseBWTNaive(bwt)

    def test_bwt_inverse_for_long_random_string(self):
        str = ''.join(random.choices(['A', 'C', 'T', 'G'], k=120000)) + '$'
        bwt = BWT(str)
        assert InverseBWT(bwt) == str

if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)
