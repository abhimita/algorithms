import unittest

def BWT(str):
    str_matrix = []
    for i in range(0, len(str)):
        text = str if i == 0 else str_matrix[i - 1]
        str_matrix.append(text[1:] + text[0])
    return ''.join([x[len(str) - 1] for x in sorted(str_matrix)])

class TestBWTTransformation(unittest.TestCase):
    def test_for_bwt(self):
        expected_results = ['AA$', 'CCCC$AAAA', 'ATG$CAAA']
        for index, text in enumerate(['AA$', 'ACACACAC$', 'AGACATA$']):
            assert BWT(text) == expected_results[index]

if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)