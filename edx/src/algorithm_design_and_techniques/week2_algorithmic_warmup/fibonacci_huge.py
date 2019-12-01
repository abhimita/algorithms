
def get_fibonacci_huge_naive(n, m):
    remainder = [0, 1]
    for i in range(2, n + 1):
        remainder.append((remainder[i - 1] + remainder[i - 2]) % m)
        # Check if we got to the period starting with 01
        if remainder[i - 1] == 0 and remainder[i] == 1:
            return remainder[n % (i - 1)]
    # Otherwise return the last element of the remainder list
    return remainder[-1]

if __name__ == '__main__':
    print(get_fibonacci_huge_naive(239, 1000))
    print(get_fibonacci_huge_naive(2816213588, 239))