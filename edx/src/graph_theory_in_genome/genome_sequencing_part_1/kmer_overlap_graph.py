#python3
import sys
import re
import unittest
import collections
import networkx as nx
import matplotlib.pyplot as plt

def overlap_graph(patterns):
    adj_list = collections.defaultdict(list)
    patterns_wo_duplicates = set()
    for p in patterns:
        patterns_wo_duplicates.add(p)

    patterns_wo_duplicates = list(patterns_wo_duplicates)
    for i in range(len(patterns_wo_duplicates)):
        suffix = patterns_wo_duplicates[i][1:]
        for j in range(len(patterns_wo_duplicates)):
            if suffix == patterns_wo_duplicates[j][:-1]:
                adj_list[i].append(j)
    return '\n'.join(['%s->%s' % (patterns_wo_duplicates[k], ','.join(map(lambda x: patterns_wo_duplicates[x], v))) for k, v in adj_list.items()])

class KmerOverlapGraph(unittest.TestCase):
    def sort_result(self, text):
        sorted_adj_list = collections.defaultdict(list)
        result = text.split('\n')
        for r in result:
            e = re.split('->', r)
            for d in e[1].split(','):
                sorted_adj_list[e[0]].append(d)
        return '\n'.join(['%s->%s' % (k, ','.join(sorted(sorted_adj_list[k]))) for k in sorted(sorted_adj_list.keys())])

    def test_more_than_two_edge_sharing_same_starting_node(self):
        patterns = ['CT', 'TG', 'TG', 'TC', 'TT', 'TC']
        expected = '\n'.join(['TT->TT,TG,TC', 'CT->TT,TG,TC', 'TC->CT'])
        actual = overlap_graph(patterns)
        assert(self.sort_result(actual) == self.sort_result(expected))
        draw_graph(actual)

    def test_nodes_in_comma_separated_list_can_act_as_source(self):
        patterns = ['GGACT', 'ACTGG', 'GACTT', 'GACTT', 'GACTG', 'ACTGG']
        expected = '\n'.join(['GGACT->GACTT,GACTG', 'GACTG->ACTGG'])
        actual = overlap_graph(patterns)
        assert(self.sort_result(actual) == self.sort_result(expected))
        draw_graph(actual)

    def test_more_than_one_edge_coming_out_of_source_node(self):
        patterns = ['GAT', 'ATG', 'ATC', 'GGA']
        expected = '\n'.join(['GAT->ATC,ATG', 'GGA->GAT'])
        actual = overlap_graph(patterns)
        assert(self.sort_result(actual) == self.sort_result(expected))
        draw_graph(actual)

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
    plt.pause(15)

unittest.main(argv=[''], verbosity=2, exit=False)
# if __name__ == "__main__":
#     #patterns = sys.stdin.read().strip().splitlines()
#     patterns = ['AAG', 'AGA', 'ATT', 'CTA', 'CTC' , 'GAT', 'TAC', 'TCT', 'TCT', 'TTC']
#     patterns = ['ACT' , 'CTT', 'TTT']
#     patterns = ['CT', 'TT', 'TT', 'TT', 'TT', 'TT']
#     patterns = ['GAT', 'ATG', 'ATC', 'GGA']
#     patterns = ['GGACT', 'ACTGG', 'GACTT', 'GACTT', 'GACTG', 'ACTGG']
#     print(overlap_graph(patterns))