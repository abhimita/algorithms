import unittest

class Node:
    def __init__(self):
        self.goto = {} # dictionary of edge labels. Key is the alphabet and value is the child node
        self.output = [] # list of valid patterns that the node represents
        self.fail = None # Link to the node where the state machine transitions when incoming character doesn't match with pattern

class AhoCorasickDFA:
    def __init__(self, patterns):
        self.patterns = patterns
        self.root = Node()
        self.results = set()

    def traverse_bfs(self):
        start = self.root
        queue = []
        queue.append(start)
        while len(queue) > 0:
            n = queue.pop(0)
            for c in n.goto.items():
                print(c[0])
                queue.append(c[1])

    def add_fail_links(self):
        start = self.root
        queue = []
        queue.append(start)
        while len(queue) > 0:
            parent = queue.pop(0)
            for child in parent.goto.items():
                queue.append(child[1])
                failed_node = parent.fail
                while failed_node is not None and child[0] not in failed_node.goto:
                    failed_node = failed_node.fail
                child[1].fail = failed_node.goto[child[0]] if failed_node is not None else self.root
                child[1].output += child[1].fail.output

    def build_dfa(self):
        for pattern in self.patterns:
            start = self.root
            for c in pattern:
                if start.goto.get(c, '') == '':
                    start.goto.update({c : Node()})
                    if start == self.root:
                        start.goto[c].fail = self.root
                start = start.goto[c]
            start.output.append(pattern)
        self.add_fail_links()

    def find_all(self, text):
        start = self.root
        for i in range(len(text)):
            while start is not None and start.goto.get(text[i], '') == '':
                start = start.fail
            if start is None:
                start = self.root
                continue
            start = start.goto[text[i]]
            if len(start.output) > 0:
                for p in start.output:
                    self.results.add(i - len(p) + 1)

def find_occurrences(text, patterns):
    dfa = AhoCorasickDFA(patterns)
    dfa.build_dfa()
    dfa.find_all(text)
    return dfa.results

def find_pattern_naive(text, patterns):
    results = []
    for pattern in patterns:
        for i in range(len(text) - len(pattern) + 1):
            found = True
            for j in range(len(pattern)):
                if pattern[j] != text[i + j]:
                    found = False
                    break
            if found and i not in results:
                results.append(i)
    return results

class TestAhoCorasickDFA(unittest.TestCase):
    def test_with_one_pattern(self):
        patterns = ['A']
        text = 'AAA'
        actual = find_occurrences(text, patterns)
        expected = find_pattern_naive(text, patterns)
        assert list(actual) == expected

    def test_with_three_patterns_having_no_occurrence(self):
        patterns = ['C', 'G', 'C']
        text = 'ATA'
        actual = find_occurrences(text, patterns)
        expected = find_pattern_naive(text, patterns)
        assert list(actual) == expected

    def test_with_three_patterns_having_multiple_occurrence(self):
        patterns = ['ATA', 'C', 'TATAT']
        text = 'ATATATA'
        actual = sorted(find_occurrences(text, patterns))
        expected = sorted(find_pattern_naive(text, patterns))
        assert list(actual) == expected

if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)