import sys

operations = [lambda x: x + 1, lambda x: x*2, lambda x: x*3]

def optimal_sequence(n):
    steps = [(float('inf'), -1)] * (n + 1)
    steps[0] = steps[1] = (0, 0)

    for i in range(1, n + 1):
        for j in range(0, len(operations)):
            index = operations[j](i)
            if index > n:
                continue
            if steps[i][0] + 1 < steps[index][0]:
                steps[index] = (steps[i][0] + 1, i)
    numbers = []
    numbers.append(n)
    index = n
    while index > 1:
        numbers.append(steps[index][1])
        index = steps[index][1]
    return reversed(numbers)

input = sys.stdin.read()
n = int(input)
sequence = list(optimal_sequence(n))
print(len(sequence) - 1)
for x in sequence:
    print(x, end=' ')
