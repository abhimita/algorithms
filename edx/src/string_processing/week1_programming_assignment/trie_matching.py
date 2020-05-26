import sys

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
        match_found = False
        for c in text[i:]:
            if tree.get(index, '') != '' and tree[index].get(c, '') != '':
                index = tree[index][c]
                if list(tree[index].keys())[0] == '$':
                    match_found = True
                    break
            else:
                break
        if match_found:
            result.append(i)
    print(result)

if __name__ == '__main__':
    solve('AATCGGGTTCAATCGGGGT', 2, ['ATCG', 'GGGT'])
    solve('AAAAC', 1, ['AAC'])
