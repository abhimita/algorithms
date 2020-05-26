#!/usr/bin/env python

# Return the trie built from patterns
# in the form of a dictionary of dictionaries,
# e.g. {0:{'A':1,'T':2},1:{'C':3}}
# where the key of the external dictionary is
# the node ID (integer), and the internal dictionary
# contains all the trie edges outgoing from the corresponding
# node, and the keys are the letters on those edges, and the
# values are the node IDs to which these edges lead.
def build_trie(patterns):
    node_number = 0
    tree = {}
    for pattern in patterns:
        index = 0
        for p in pattern:
            if tree.get(index, '') == '' or tree[index].get(p, '') == '':
                if tree.get(index, '') == '':
                    tree[index] = {}
                tree[index].update({p: node_number + 1})
                node_number += 1
                index = node_number
            else:
                index = tree[index][p]
    print(tree)
    return tree


if __name__ == '__main__':
    patterns = ['ATA', 'ATAGC']
    tree = build_trie(patterns)
    for node in tree:
        for c in tree[node]:
            print("{}->{}:{}".format(node, tree[node][c], c))