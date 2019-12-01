from gcd import gcd
def lcm(a, b):
    return (a*b) // gcd(a, b)

if __name__ == '__main__':
    print(lcm(226553150000000000000000, 1023473145))