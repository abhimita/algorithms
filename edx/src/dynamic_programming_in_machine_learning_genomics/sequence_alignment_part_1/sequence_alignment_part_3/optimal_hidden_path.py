import sys
import unittest

# Input:
# A string x emitted by an HMM (Σ, States, Transition, Emission).

# Output:
# A path π that maximizes the probability Pr(x, π) over all possible paths through this HMM.
# Please be as close to the book as possible.

# Input Format.
# The first line of the input contains the outcome string x.
# The second line of the input is “--------” (a delimiter).
# The third line of the input is the list of symbols in the alphabet Σ (space-separated).
# The fourth line of the input is “--------” (a delimiter).
# The fifth line of the input is the list of states States (space-separated).
# The sixth line of the input is “--------” (a delimiter).
# The next |States|+1 lines are the transition matrix Transition, depicted as a
# tab-delimited |States| by |States| matrix as shown in the sample dataset.
# The next line is “--------” (a delimiter).
# The remaining lines are the emission matrix Emission, depicted as a
# tab-delimited |States| by |Σ| matrix as shown in the sample dataset.
# You may assume that transitions from the initial state occur with equal probability.

# Output Format.
# A path π that maximizes the probability Pr(x, π) over all possible paths through this HMM.
# Each probability should be written to at least 3 decimal places. (Note: more than one solution may exist,
# in which case you may output any one.)

# Constraints. |x| = |π| = 100; 2 ≤ |States| ≤ 4; |Σ| = 3

def optimal_path(x, sigma, states, transition, emission):
    transition['S'] = dict([(s, 1.0 / len(states)) for s in states])

    previous_nodes = ['S']
    state_values = []
    state_values.append({'S': (1, None)})
    hidden_path = []

    for i, e in enumerate(x):
        node_values = dict([(s, (float('-inf'), None)) for s in states])

        for s in states:
            for p in previous_nodes:
                if state_values[i][p][0] * transition[p][s] * emission[s][e] > node_values[s][0]:
                    node_values[s] = (state_values[i][p][0] * transition[p][s] * emission[s][e], p)
        previous_nodes = states
        state_values.append(node_values)

    i = len(state_values) - 1
    state = list(dict([sorted(state_values[i].items(), key=lambda x: x[1][0], reverse=True)[0]]).keys())[0]
    hidden_path.append(state)
    while i > 0:
        state = state_values[i][state][1]
        hidden_path.append(state)
        i = i - 1

    return ''.join(reversed(hidden_path))[1:]

class TestOptimalHiddenPath(unittest.TestCase):

    def test_base_case(self):
        x = 'xyxzz'
        sigma = ['x', 'y', 'z']
        states = ['A', 'B']
        transition = {'A': {'A': 0.641, 'B': 0.359},
                      'B': {'A': 0.729, 'B': 0.271}}
        emission = {'A': {'x': 0.117, 'y': 0.691, 'z': 0.192},
                    'B': {'x': 0.097, 'y': 0.42, 'z': 0.483}}
        assert optimal_path(x,sigma,states,transition,emission) == 'AAABA'

    def test_emission_probability_is_used_for_emitted_code(self):
        x = 'xyxy'
        sigma = ['x', 'y']
        states = ['A', 'B']
        transition = {'A': {'A': 0.5, 'B': 0.5},
                      'B': {'A': 0.5, 'B': 0.5}}
        emission = {'A': {'x': 0.1, 'y': 0.9},
                    'B': {'x': 0.9, 'y': 0.1}}
        assert optimal_path(x,sigma,states,transition,emission) == 'BABA'

    def test_transition_probability_is_used_for_optimal_path(self):
        x = 'xyxy'
        sigma = ['x', 'y']
        states = ['A', 'B']
        transition = {'A': {'A': 0.9, 'B': 0.1},
                      'B': {'A': 0.1, 'B': 0.9}}
        emission = {'A': {'x': 0.5, 'y': 0.5},
                    'B': {'x': 0.5, 'y': 0.5}}
        assert optimal_path(x,sigma,states,transition,emission) in ['AAAA', 'BBBB']

    def test_when_string_is_one_character_long(self):
        x = 'x'
        sigma = ['x', 'y']
        states = ['A', 'B']
        transition = {'A': {'A': 0.4, 'B': 0.6},
                      'B': {'A': 0.2, 'B': 0.8}}
        emission = {'A': {'x': 0.55, 'y': 0.45},
                    'B': {'x': 0.5, 'y': 0.5}}
        assert optimal_path(x,sigma,states,transition,emission) == 'A'

    def test_when_hmm_has_one_state_only(self):
        x = 'zxyxy'
        sigma = ['x', 'y', 'z']
        states = ['A']
        transition = {'A': {'A': 1.0}}
        emission = {'A': {'x': 0.5, 'y': 0.5, 'z': 0}}
        assert optimal_path(x,sigma,states,transition,emission) == 'AAAAA'

    def test_code_is_not_using_greedy_strategy(self):
        x = 'xx'
        sigma = ['x', 'y']
        states = ['A', 'B', 'C']
        transition = {'A': {'A': 0.7, 'B': 0.1, 'C': 0.2},
                      'B': {'A': 0.5, 'B': 0.3, 'C': 0.2},
                      'C': {'A': 1.0, 'B': 0.0, 'C': 0.0}}
        emission = {'A': {'x': 0.0, 'y': 1.0},
                    'B': {'x': 0.5, 'y': 0.5},
                    'C': {'x': 1.0, 'y': 0.0}}
        assert optimal_path(x,sigma,states,transition,emission) == 'BC'

unittest.main(argv=[''], verbosity=2, exit=False)