# python3
import unittest


# Find the minimum number of coins needed to make change.

# Input: An integer money and an integer array Coins = (coin1, ..., coind).
# Output: The minimum number of coins with denominations Coins that changes money

# Imagine that you bought a textbook for $69.24, which you paid for with $70 in cash.
# You are due 76 cents in change, and the cashier now must make a decision whether to
# give you a fistful of 76 1-cent coins or just four coins (25 + 25 + 25 + 1 = 76).
# Making change in this example is easy, but it casts light on a more general problem:
# how can a cashier make change using the fewest number of coins? Different currencies
# have different possible coin values, or denominations. In the US, the coin denominations
# are (1, 5, 10, 25, 50 100); in the Roman Republic before Julius Caesar’s assassination,
# they were (1, 4, 5, 10, 24, 30, 40, 120).

# Input Format. The first line of the input contains the positive integer money.
# The second line contains a comma-delimited list of positive integers Coins.

# Output Format. The minimum number of coins with denominations Coins that changes money.
# Constraints. money ≤ 20,000; |Coins| ≤ 7, 1 ≤ all coin denominations ≤ 100

def find_change(money, coins):
    min_coins = [0] * (money + 1)
    min_coins[0] = 0
    coins = sorted(coins)
    for m in range(1, money + 1):
        min_change = float('inf')
        for c in coins:
            if c > m: break
            min_change = min(min_change, min_coins[m - c] + 1)
        min_coins[m] = min_change
    return min_coins[-1]

# This is an extension of min number of coins problem
# This function keeps track of the changes used and returns them as list
def find_min_change_denominations(money, coins):
    min_coins = [0] * (money + 1)
    min_coins[0] = 0
    min_denominations = [0] * (money + 1)
    min_denominations[0] = 0

    coins = sorted(coins)
    for m in range(1, money + 1):
        min_change = float('inf')
        min_index = -1
        for c in coins:
            if c > m: break
            if min_change > min_coins[m - c] + 1:
                min_change = min_coins[m - c] + 1
                min_index = m - c
        min_coins[m] = min_change
        min_denominations[m] = min_index
    i = len(min_denominations) - 1
    coins_used = []
    while i > 0:
        coins_used.append(i - min_denominations[i])
        i = min_denominations[i]
    return sorted(coins_used)

class TestFindChange(unittest.TestCase):
    def test_where_greedy_algorithm_fails(self):
        money = 12
        coins = [9, 6, 1]
        assert find_change(money, coins) == 2
        assert find_min_change_denominations(money, coins) == [6, 6]

    def test_correctness_of_final_return_value(self):
        money = 13
        coins = [1, 5]
        assert find_change(money, coins) == 5
        assert find_min_change_denominations(money, coins) == [1, 1, 1, 5, 5]

    def test_first_coin_is_considered(self):
        money = 10
        coins = [10, 5, 4, 3, 2, 1]
        assert find_change(money, coins) == 1
        assert find_min_change_denominations(money, coins) == [10]

    def test_last_coin_is_considered(self):
        money = 10
        coins = [1, 2, 3, 4, 5, 10]
        assert find_change(money, coins) == 1
        assert find_min_change_denominations(money, coins) == [10]

    def test_base_case(self):
        money = 7
        coins = [1, 5]
        assert find_change(money, coins) == 3
        assert find_min_change_denominations(money, coins) == [1, 1, 5]


unittest.main(argv=[''], verbosity=2, exit=False)
