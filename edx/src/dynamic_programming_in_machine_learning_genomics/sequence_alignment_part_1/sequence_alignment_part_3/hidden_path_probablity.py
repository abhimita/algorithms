#python3
import sys
import unittest

# Compute the probability of a hidden path in an HMM.
# Input: A hidden path π in an HMM (Σ, States, Transition, Emission).
# Output: The probability of this path, Pr(π).
# Input Format. The first line of the input contains the path π in the HMM The second line of the
# input is “--------” (a delimiter). The third line of the input is the list of states States (space-separated).
# The fourth line of the input is “--------” (a delimiter). The remaining lines are the transition matrix
# Transition, depicted as a tab-delimited |States| by |States| matrix. You may assume that transitions
# from the initial state occur with equal probability.
# Output Format. The probability of this path, Pr(π), to at least 3 significant figures.
# Constraints. 50 ≤ |π| ≤ 100; |States| = 10

def path_probability(pi, states, transition):
    p_pi = 1.0 / len(states)
    last_state = pi[0]
    for i in range(1, len(pi)):
        new_state = pi[i]
        p_pi = p_pi * transition[last_state][new_state]
        last_state = new_state
    return '{0:1.4e}'.format(p_pi)

class TestHiddenPathProbablity(unittest.TestCase):
    def test_base_case(self):
        pi = 'ABABB'
        states = ['A', 'B']
        transition = {'A': {'A':  0.377, 'B': 0.623}, 'B' : {'A': 0.26, 'B': 0.74}}
        assert path_probability(pi,states,transition) == '3.7338e-02'

    def test_correct_initial_transition_probablity_is_used(self):
        pi = 'A'
        states = ['A', 'B']
        transition = {'A': {'A':  0.425, 'B': 0.575}, 'B' : {'A': 0.228, 'B': 0.772}}
        assert path_probability(pi,states,transition) == '5.0000e-01'

    def test_correct_parsing_of_input_path(self):
        pi = 'AAB'
        states = ['A', 'B']
        transition = {'A': {'A':  1, 'B': 0}, 'B' : {'A': 0.5, 'B': 0.5}}
        assert path_probability(pi,states,transition) == '0.0000e+00'

    def test_output_is_at_least_three_significant_digits(self):
        pi = 'BCAACAADD'
        states = ['A', 'B', 'C', 'D']
        transition = {'A': {'A':  0.1, 'B': 0, 'C': 0.3, 'D': 0.6},
                      'B': {'A':  0.5, 'B': 0.4, 'C': 0.1, 'D': 0},
                      'C': {'A':  0.3, 'B': 0.3, 'C': 0.3, 'D': 0.1},
                      'D': {'A':  0.2, 'B': 0.5, 'C': 0.1, 'D': 0.2}}

        assert path_probability(pi,states,transition) == '8.1000e-07'

unittest.main(argv=[''], verbosity=2, exit=False)
