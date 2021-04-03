#python3
import sys
import unittest

# Find the probability that an HMM emits a given string.

# Input:
# A string x emitted by an HMM (Σ, States, Transition, Emission).
# Output:
# The probability Pr(x) that the HMM emits x.
# Input Format.
# The first line of the input contains the outcome string x.
# The second line of the input is “--------” (a delimiter).
# The third line of the input is the list of symbols in the alphabet Σ (space-separated).
# The fourth line of the input is “--------” (a delimiter).
# The fifth line of the input is the list of states States (space-separated).
# The sixth line of the input is “--------” (a delimiter).
# The next |States|+1 lines are the transition matrix Transition, depicted as a
# tab-delimited |States| by |States| matrix as shown in the sample dataset.
# The next line is “--------” (a delimiter). The remaining lines are the emission
# matrix Emission, depicted as a tab-delimited |States| by |Σ| matrix as shown in the sample dataset.
# You may assume that transitions from the initial state occur with equal probability.
# Output Format.
# The probability Pr(x) that the HMM emits x to at least 3 significant figures.
# Constraints. |x| = |π| = 100; 2 ≤ |States| ≤ 4; |Σ| = 3

def outcome_likelihood(x, sigma, states, transition, emission):
    transition['S'] = dict([(s, 1.0 / len(states)) for s in states])

    previous_nodes = ['S']
    state_values = []
    state_values.append({'S': 1})

    for i, e in enumerate(x):
        node_values = dict([(s, 0) for s in states])
        for s in states:
            for p in previous_nodes:
                node_values[s] += state_values[i][p] * transition[p][s] * emission[s][e]
        previous_nodes = states
        state_values.append(node_values)
    return '{0:1.6e}'.format(sum(list(state_values[-1].values())))

class TestOutcomeLikekihood(unittest.TestCase):

    def test_base_case(self):
        x = 'xzyyz'
        sigma = ['x', 'y', 'z']
        states = ['A', 'B']
        transition = {'A': {'A': 0.303, 'B': 0.697},
                      'B': {'A': 0.831, 'B': 0.169}}
        emission = {'A': {'x': 0.533, 'y': 0.065, 'z': 0.402},
                    'B': {'x': 0.342, 'y': 0.334, 'z': 0.324}}

        assert outcome_likelihood(x, sigma, states, transition, emission) == '1.546734e-03'

    def test_correct_application_of_transition_from_initial_state(self):
        x = 'x'
        sigma = ['x']
        states = ['A', 'B']
        transition = {'A': {'A': 0.5, 'B': 0.5},
                      'B': {'A': 0.5, 'B': 0.5}}
        emission = {'A': {'x': 0.5},
                    'B': {'x': 0.5}}

        assert outcome_likelihood(x, sigma, states, transition, emission) == '5.000000e-01'

    def test_correct_parsing_of_emitted_string(self):
        x = 'xy'
        sigma = ['x', 'y']
        states = ['A', 'B']
        transition = {'A': {'A': 0.4, 'B': 0.6},
                      'B': {'A': 0.6, 'B': 0.4}}
        emission = {'A': {'x': 0.7, 'y': 0.3},
                    'B': {'x': 0.4, 'y': 0.6}}

        assert outcome_likelihood(x, sigma, states, transition, emission) == '2.520000e-01'

    def test_zero_likelihood(self):
        x = 'xzywyxw'
        sigma = ['w', 'x', 'y', 'z']
        states = ['A', 'B', 'C']
        transition = {'A': {'A': 0.7, 'B': 0.1, 'C': 0.2},
                      'B': {'A': 0.5, 'B': 0.3, 'C': 0.2},
                      'C': {'A': 0.1, 'B': 0.4, 'C': 0.5}}
        emission = {'A': {'w': 0.34, 'x': 0.24, 'y': 0.42, 'z': 0},
                    'B': {'w': 0.17, 'x': 0.49, 'y': 0.34, 'z': 0},
                    'C': {'w': 0.22, 'x': 0.22, 'y': 0.56, 'z': 0}}

        assert outcome_likelihood(x, sigma, states, transition, emission) == '0.000000e+00'

    def test_output_at_least_three_significant_figures(self):
        x = 'xxxxyxxxzz'
        sigma = ['x', 'y', 'z']
        states = ['A', 'B', 'C']
        transition = {'A': {'A': 0.7, 'B': 0.1, 'C': 0.2},
                      'B': {'A': 0.5, 'B': 0.3, 'C': 0.2},
                      'C': {'A': 0.1, 'B': 0.4, 'C': 0.5}}
        emission = {'A': {'x': 0.24, 'y': 0.41, 'z': 0.01},
                    'B': {'x': 0.49, 'y': 0.33, 'z': 0.01},
                    'C': {'x': 0.22, 'y': 0.55, 'z': 0.01}}

        assert outcome_likelihood(x, sigma, states, transition, emission) == '9.167710e-09'

unittest.main(argv=[''], verbosity=2, exit=False)