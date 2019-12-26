
def are_matching(left, right):
    matched = { '{' : '}', '[': ']', '(' : ')'}
    return matched[left] == right

def find_mismatch(str):
    stack = []
    position = 0
    for s in str:
        position += 1
        if s in ['[', '(',  '{']:
            stack.append((s, position))
        elif s in [']', '}', ')']:
            if len(stack) > 0:
                symbol, symbol_pos = stack.pop()
                if are_matching(symbol, s):
                    continue
                else:
                    return position
            else:
                return position

    if len(stack) > 0:
        return stack.pop()[1]
    else:
        return 'Success'

if __name__ == '__main__':
    print(check_bracket('{{pqr}}()'))

