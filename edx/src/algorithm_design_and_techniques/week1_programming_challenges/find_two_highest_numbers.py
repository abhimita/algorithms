
import random
import math

def max_pairwise_product_efficient(a):
    highest = a[0] if a[0] > a[1] else a[1]
    next_highest = a[1] if highest == a[0] else a[0]
    for i in a[2:]:
        if i > highest:
            highest, next_highest = i, highest
        elif i <= highest and i > next_highest:
            next_highest = i
    result = highest * next_highest
    return result

def max_pairwise_product_brute(a):
    highest, next_highest = sorted(a)[-2:]
    result = highest * next_highest
    return result

if __name__ == '__main__':
    for i in range(0, 10000):
        n = random.randint(2, math.pow(10, 5))
        a = [random.randint(2, math.pow(10, 5)) for i in range(0, n)]
        assert(len(a) == n)
        x = max_pairwise_product_efficient(a)
        y = max_pairwise_product_brute(a)
        assert(x == y)
