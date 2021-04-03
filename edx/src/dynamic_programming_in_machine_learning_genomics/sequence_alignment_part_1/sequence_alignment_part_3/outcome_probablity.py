import sys
import unittest

# Compute the probability that an HMM will emit a string given its hidden path.

# Input: A string x emitted by an HMM (Σ, States, Transition, Emission) and a hidden path π.

# Output: The conditional probability Pr(x|π) that x will be emitted given that the HMM follows the hidden path π.

# Input Format. The first line of the input contains the outcome string x.
# The second line of the input is “--------” (a delimiter).
# The third line of the input is the list of symbols in the alphabet Σ (space-separated).
# The fourth line of the input is “--------” (a delimiter).
# The fifth line of the input contains the hidden path π.
# The sixth line of the input is “--------” (a delimiter).
# The seventh line of the input is the list of states States (space-separated).
# The eighth line of the input is “--------” (a delimiter).
# The remaining lines are the emission matrix Emission, depicted as
# a tab-delimited |States| by |Σ| matrix as shown in the sample dataset.
# You may assume that transitions from the initial state occur with equal probability.
# Output Format. The conditional probability Pr(x|π) that x will be emitted given that the HMM
# follows the hidden path π. Your answer should be accurate up to at least 3 significant figures.
# For example, if the answer is 0.001234678 (three significant figures are shown in bold) then
# even an imprecise answer like 0.00123 will be accepted by the grader because it is within 0.00001
# from the correct solution.

# Constraints. |x| = |π| = 50; |States| = 2; |Σ| = 3

def outcome_probability(x, sigma, pi, states, emission):
    p = 1.0
    for i in range(0, len(x)):
        state = pi[i]
        emitted_char = x[i]
        p = p * emission[state][emitted_char]
    return '{0:1.6e}'.format(p)

class TestOutcomeProbablity(unittest.TestCase):
    def test_base_case(self):
        x = 'zzzyx'
        sigma = ['x', 'y', 'z']
        pi = 'BAAAA'
        states = ['A', 'B']
        emission = {'A': {'x': 0.176, 'y': 0.596, 'z': 0.228},
                    'B': {'x': 0.225, 'y': 0.572, 'z': 0.203}}
        assert outcome_probability(x, sigma, pi, states, emission) == '1.106941e-03'

    def test_when_path_is_one_character_long(self):
        x = 'x'
        sigma = ['x', 'y', 'z']
        pi = 'A'
        states = ['A', 'B']
        emission = {'A': {'x': 1},
                    'B': {'x': 1}}
        assert outcome_probability(x, sigma, pi, states, emission) == '1.000000e+00'

    def test_parsing_of_emission_matrix(self):
        x = 'xx'
        sigma = ['x', 'y']
        pi = 'AB'
        states = ['A', 'B']
        emission = {'A': {'x': 0.6, 'y': 0.4},
                    'B': {'x': 0.3, 'y': 0.7}}
        assert outcome_probability(x, sigma, pi, states, emission) == '1.800000e-01'

    def test_when_different_characters_are_emitted_by_same_state(self):
        x = 'xy'
        sigma = ['x', 'y']
        pi = 'AA'
        states = ['A', 'B']
        emission = {'A': {'x': 0.6, 'y': 0.4},
                    'B': {'x': 0.3, 'y': 0.7}}
        assert outcome_probability(x, sigma, pi, states, emission) == '2.400000e-01'

    def test_output_has_at_least_three_significant_figures(self):
        x = 'xxxxxyxyyx'
        sigma = ['x', 'y']
        pi = 'AABBABABBA'
        states = ['A', 'B']
        emission = {'A': {'x': 0.01, 'y': 0.99},
                    'B': {'x': 0.01, 'y': 0.99}}
        assert outcome_probability(x, sigma, pi, states, emission) == '9.702990e-15'

unittest.main(argv=[''], verbosity=2, exit=False)
