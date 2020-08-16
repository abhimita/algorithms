#python3
import sys
import unittest
import collections
import re
import networkx as nx
import matplotlib.pyplot as plt

def de_bruijn(k, text):
    adj_list = collections.defaultdict(list)
    for i in range(len(text) - k + 1):
        k_mer = text[i : i + k]
        adj_list[k_mer[:-1]].append(k_mer[1:])
    return '\n'.join(['%s->%s' % (k, ','.join(adj_list[k])) for k in adj_list.keys()])

class DeBruijnGraph(unittest.TestCase):
    def sort_result(self, text):
        sorted_adj_list = collections.defaultdict(list)
        result = text.split('\n')
        for r in result:
            e = re.split('->', r)
            for d in e[1].split(','):
                sorted_adj_list[e[0]].append(d)
        return '\n'.join(['%s->%s' % (k, ','.join(sorted(sorted_adj_list[k]))) for k in sorted(sorted_adj_list.keys())])


    def test_multiple_occurrences_of_same_kmer(self):
        text = 'GCTTCTTC'
        k = 4
        expected = ['GCT->CTT', 'CTT->TTC,TTC', 'TTC->TCT', 'TCT->CTT']
        actual = de_bruijn(k, text)
        draw_graph(actual)
        assert(self.sort_result('\n'.join(expected)) == self.sort_result(actual))

    def test_multiple_edges_sharing_a_node(self):
        text = 'CCTCCG'
        k = 3
        expected = ['CC->CT,CG', 'CT->TC', 'TC->CC']
        actual = de_bruijn(k, text)
        draw_graph(actual)
        assert(self.sort_result('\n'.join(expected)) == self.sort_result(actual))

    def test_input_string_is_split_along_kmers(self):
        text = 'AGCCT'
        k = 4
        expected = ['AGC->GCC', 'GCC->CCT']
        actual = de_bruijn(k, text)
        draw_graph(actual)
        assert(self.sort_result('\n'.join(expected)) == self.sort_result(actual))

    def test_with_node_having_two_outgoing_edges(self):
        text = 'ACGTGTATA'
        k = 3
        expected = ['AC->CG', 'CG->GT', 'GT->TG,TA', 'TG->GT', 'TA->AT', 'AT->TA']
        actual = de_bruijn(k, text)
        draw_graph(actual)
        assert(self.sort_result('\n'.join(expected)) == self.sort_result(actual))

    def test_with_repeated_kmer(self):
        text = 'TTTTTTTTTT'
        k = 5
        expected = ['TTTT->TTTT,TTTT,TTTT,TTTT,TTTT,TTTT']
        actual = de_bruijn(k, text)
        draw_graph(actual)
        assert(self.sort_result('\n'.join(expected)) == self.sort_result(actual))

def draw_graph(actual):
    fig = plt.figure(figsize=(4,4))
    plt.ion()
    plt.show()
    G = nx.MultiDiGraph()
    result = actual.split('\n')
    for r in result:
        e = re.split('->', r)
        for d in e[1].split(','):
            G.add_edge(e[0], d)
    layout = nx.drawing.nx_agraph.pygraphviz_layout(G)
    nx.draw(G, layout, with_labels=True)
    plt.show()
    plt.pause(5)

unittest.main(argv=[''], verbosity=2, exit=False)