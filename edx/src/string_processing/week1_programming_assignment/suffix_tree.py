import sys

def maximal_match(str1, str2):
    index = 0
    for i in range(0, min(len(str1), len(str2))):
        if str1[i] == str2[i]:
            index += 1
        else:
            break
    return index

def get_suffixes(str):
    for i in range(0, len(str)):
        yield str[i : len(str)]

def build_suffix_tree(text):
    tree = {}
    last_index = 0
    for suffix_pos, suffix in enumerate(get_suffixes(text)):
        index = 0
        if tree.get(index, '') == '':
            tree[index] = {}
            tree[index].update({suffix: suffix_pos})
            last_index += 1
        else:
            partial_match_found = False
            while not partial_match_found:
                for k in tree[index].items():
                    match_index = maximal_match(k[0], suffix)
                    if match_index > 0:
                        if match_index == len(k[0]):
                            index = k[1]
                            suffix = suffix[match_index:]
                            break
                        else:
                            partial_match_found = True
                            tree[index].update({k[0][:match_index]: last_index})
                            tree[last_index] = {}
                            tree[last_index].update({k[0][match_index:] : k[1]})
                            tree[last_index].update({suffix[match_index:]: suffix_pos})
                            last_index += 1
                            del tree[index][k[0]]
                            break
                if match_index == 0:
                    tree[index].update({suffix: suffix_pos})
                    break
    edges = []
    for e in tree.items():
        edges.extend(list(e[1].keys()))
    return edges

if __name__ == '__main__':
    text = sys.stdin.readline().strip()
    result = build_suffix_tree(text)
    print("\n".join(result))