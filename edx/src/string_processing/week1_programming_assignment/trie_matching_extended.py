import unittest

def build_trie(patterns):
    tree = {}
    node_number = 0
    for pos, pattern in enumerate(patterns):
        index = 0
        for s in pattern:
            if tree.get(index, '') == '' or tree[index].get(s, '') == '':
                if tree.get(index, '') == '':
                    tree[index] = {}
                tree[index].update({s: node_number + 1})
                node_number = node_number + 1
                index = node_number
            else:
                index = tree[index][s]
    return tree

def solve(text, n , patterns):
    tree = build_trie(map(lambda x: x + '$', patterns))
    result = []
    min_pattern_length = min(list(map(len, patterns)))
    for i in range(0, len(text) - min_pattern_length + 1):
        index = 0
        for c in text[i:]:
            if tree.get(index, '') != '' and tree[index].get(c, '') != '':
                index = tree[index][c]
                for m in list(tree[index].keys()):
                    if m == '$':
                        if len(result) == 0 or (len(result) > 0 and result[len(result) - 1] != i):
                            result.append(i)
            else:
                break
    return result

def solve_brute(text, n, patterns):
    results = set()
    for p in patterns:
        i = 0
        while True:
            if i >= len(text) - len(p) + 1:
                break
            index = text[i:].find(p)
            if index == -1:
                break
            else:
                results.add(i + index)
                i += (index + 1)
    return list(results)

class TestTrieMatchingExtended(unittest.TestCase):
    def execute(self, text, patterns):
        actual = solve(text, len(patterns), patterns)
        expected = solve_brute(text, len(patterns), patterns)
        assert sorted(actual) == sorted(expected)

    def test_matching_two_patterns_against_text(self):
        patterns = ['ATCG', 'GGGT']
        text = 'AATCGGGTTCAATCGGGGT'
        self.execute(text, patterns)

    def test_matching_four_patterns_against_text(self):
        patterns = ['ATA', 'AT', 'CA', 'AC']
        text = 'ACATA'
        self.execute(text, patterns)

if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)
