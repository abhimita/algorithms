def gcd(a, b):
    a, b = max(a, b), min(a, b)
    while True:
        r = a % b
        if r == 0:
            return b
        else:
            a, b = b, r


