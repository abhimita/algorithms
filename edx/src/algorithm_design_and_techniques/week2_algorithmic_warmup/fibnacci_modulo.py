
def fib(n):
    if n <= 1:
        return n
    prev, current = 0, 1
    for i in range(2, n + 1):
        prev, current = current, prev + current
    return current

def fib_mod(n, m):
    remainder = [0, 1]
    for i in range(2, n + 1):
        remainder.append((remainder[i - 1] + remainder[i - 2]) % m)
        if remainder[i - 1] == 0 and remainder[i] == 1:
            return remainder[n % (i - 1)]
    return remainder[len(remainder) - 1]

if __name__ == '__main__':
    print(fib_mod(2816213588, 239))
    print(fib_mod(2005, 3))