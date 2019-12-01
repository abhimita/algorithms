def calc_fib(n):
    if n <= 1:
        return n
    prev = 0
    num = 1
    for i in range(2, n + 1):
        num, prev = prev + num, num
    return num

if __name__ == '__main__':
    n = int(20)
    print(calc_fib(n))