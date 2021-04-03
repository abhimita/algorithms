#!/usr/env/bin python

import unittest

# Given a value N, if we want to make change for N cents, and we have infinite supply of
# each of S = { S1, S2, .. , Sm} valued coins, how many ways can we make the change?
# The order of coins doesn’t matter.
# For example, for N = 4 and S = {1,2,3}, there are four solutions: {1,1,1,1},{1,1,2},{2,2},{1,3}.
# So output should be 4.
# For N = 10 and S = {2, 5, 3, 6}, there are five solutions: {2,2,2,2,2}, {2,2,3,3}, {2,2,6}, {2,3,5} and {5,5}.
# So the output should be 5

def change_coins(money, coins):
    if money == 0:
        return 1
    if money < 0:
        return 0
    if len(coins) == 0 and money >= 1:
        return 0
    return change_coins(money - coins[0], coins) + change_coins(money, coins[1:])

class TestChangeCoins(unittest.TestCase):
    def test_with_three_coin_denominations(self):
        assert change_coins(4, [1, 2, 3]) == 4

    def test_with_four_coin_denominations(self):
        assert change_coins(10, [2, 5, 3, 6]) == 5

unittest.main(argv=[''], verbosity=2, exit=False)