
def get_change(value, coins=[1, 3, 4]):
    changes = [float('inf')] * (value + 1)
    changes[0] = 0
    denominations = {}
    for i in range(1, value + 1):
        for j in range(0, len(coins)):
            if i - coins[j] < 0: continue
            changes[i] = min(changes[i], changes[i - coins[j]] + 1)
    return(changes[-1])

if __name__ == '__main__':
    print(get_change(17, [1, 3, 4]))
    print(get_change(9, [1, 3, 4]))
