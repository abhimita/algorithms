#!/usr/bin/env python

import math
import pprint as pp
import sys

states = ['S', 'H', 'L']
state_to_id = dict([(s, i) for i, s in enumerate(states)])
sigma = ['A', 'C', 'G', 'T']
sigma_to_id = dict([(s, i) for i, s in enumerate(sigma)])
transition_matrix = [[0, 0.5, 0.5], [0, 0.5, 0.5], [0, 0.4, 0.6]]
emission_matrix = [[0, 0, 0, 0], [0.2, 0.3, 0.3, 0.2], [0.3, 0.2, 0.2, 0.3]]
str_sequence = "GGCACTGAA"

# change values to log scale
transition_matrix = [list(map(lambda x: 0 if x == 0 else math.log2(x), row)) for row in transition_matrix]
emission_matrix = [list(map(lambda x: 0 if x == 0 else math.log2(x), row)) for row in emission_matrix]

row = [0 for _ in range(0, len(str_sequence))]
dp = [row[0:] for s in states]

for current_state in states[1:]:
    dp[state_to_id[current_state]][0] = \
        transition_matrix[state_to_id['S']][state_to_id[current_state]] + \
        emission_matrix[state_to_id[current_state]][sigma_to_id[str_sequence[0]]]

for i, c in enumerate(str_sequence[1:]):
    for current_state in states[1:]:
        max_value = float('-inf')
        for previous_state in states[1:]:
            value = dp[state_to_id[previous_state]][i] + \
                    transition_matrix[state_to_id[previous_state]][state_to_id[current_state]]
            if value > max_value:
                max_value = value
        dp[state_to_id[current_state]][i + 1] = emission_matrix[state_to_id[current_state]][sigma_to_id[c]] + max_value

pp.pprint([list(map(lambda x: round(x, 3), r)) for r in dp])





