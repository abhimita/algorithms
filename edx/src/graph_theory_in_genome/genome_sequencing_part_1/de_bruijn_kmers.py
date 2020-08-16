#python3
import sys
import unittest
import collections
import re

def de_bruijn(patterns):
    adj_list = collections.defaultdict(list)
    for p in patterns:
        src = p[:-1]
        dst = p[1:]
        adj_list[src].append(dst)
    return '\n'.join(['%s->%s' % (k, ','.join(adj_list[k])) for k in adj_list])

class TestDeBruijn(unittest.TestCase):
    def sort_result(self, text):
        sorted_adj_list = collections.defaultdict(list)
        result = text.split('\n')
        for r in result:
            e = re.split('->', r)
            for d in e[1].split(','):
                sorted_adj_list[e[0]].append(d)
        return '\n'.join(['%s->%s' % (k, ','.join(sorted(sorted_adj_list[k]))) for k in sorted(sorted_adj_list.keys())])

    def test_two_edges_from_source_to_destination(self):
        patterns = ['GAGG', 'CAGG', 'GGGG', 'GGGA', 'CAGG', 'AGGG', 'GGAG']
        expected = ['GAG->AGG', 'CAG->AGG,AGG', 'GGG->GGG,GGA', 'AGG->GGG', 'GGA->GAG']
        actual = de_bruijn(patterns)
        assert(self.sort_result('\n'.join(expected)) == self.sort_result(actual))

    def test_all_kmers_are_processed(self):
        patterns = ['GCAAG', 'CAGCT', 'TGACG']
        expected = ['GCAA->CAAG', 'CAGC->AGCT', 'TGAC->GACG']
        actual = de_bruijn(patterns)
        assert(self.sort_result('\n'.join(expected)) == self.sort_result(actual))

    def test_edges_sharing_same_node(self):
        patterns = ['AGGT', 'GGCT', 'AGGC']
        expected = ['AGG->GGT,GGC', 'GGC->GCT']
        actual = de_bruijn(patterns)
        assert(self.sort_result('\n'.join(expected)) == self.sort_result(actual))

    def test_handling_duplicate_patterns(self):
        patterns = ['TTCT', 'GGCT', 'AAGT', 'GGCT', 'TTCT']
        expected = ['TTC->TCT,TCT', 'GGC->GCT,GCT', 'AAG->AGT']
        actual = de_bruijn(patterns)
        assert(self.sort_result('\n'.join(expected)) == self.sort_result(actual))

    def test_more_than_two_edges_sharing_start_node(self):
        patterns = ['CA', 'CA', 'CA', 'CA', 'CC', 'CA']
        expected = ['C->A,A,A,A,C,A']
        actual = de_bruijn(patterns)
        assert(self.sort_result('\n'.join(expected)) == self.sort_result(actual))

unittest.main(argv=[''], verbosity=2, exit=False)

