#python3
import sys
import unittest

def estimate_parameters(x, sigma, pi, states):
    row = [0.0 for _ in range(len(states))]
    transition_matrix = [row[0:] for _ in range(len(states))]
    row = [0.0 for _ in range(len(sigma))]
    emission_matrix = [row[0:] for _ in range(len(states))]

    state_to_id = dict([(s, i) for i, s in enumerate(states)])
    sigma_to_id = dict([(s, i) for i, s in enumerate(sigma)])

    emission_matrix[state_to_id[pi[0]]][sigma_to_id[x[0]]] += 1
    for i in range(1, len(pi)):
        transition_matrix[state_to_id[pi[i - 1]]][state_to_id[pi[i]]] += 1
        emission_matrix[state_to_id[pi[i]]][sigma_to_id[x[i]]] += 1

    for i, r in enumerate(transition_matrix):
        s = sum(r)
        if s > 0:
            transition_matrix[i] = [e/s for e in r]
        else:
            transition_matrix[i] = [1.0/len(r) for _ in r]

    scale_matrix(transition_matrix)
    scale_matrix(emission_matrix)
    return ' '.join(states) + '\n' + \
          '\n'.join([' '.join([states[i]] + list(map(str, r))) for i, r in enumerate(transition_matrix)]) + '\n' + \
          '--------' + '\n' + \
          ' '.join(sigma) + '\n' + \
          '\n'.join([' '.join([states[i]] + list(map(str, r))) for i, r in enumerate(emission_matrix)])


def scale_matrix(matrix):
    for i, r in enumerate(matrix):
        s = sum(r)
        if s > 0:
            matrix[i] = [round(e/s, 3) for e in r]
        else:
            matrix[i] = [round(1.0/len(r), 3) for _ in r]

class TestParameterEstimation(unittest.TestCase):

    def test_base_case(self):
        assert estimate_parameters(
            x="yzzzyxzxxx",
            sigma=['x', 'y', 'z'],
            pi='BBABABABAB',
            states=['A', 'B', 'C']) == """A B C
A 0.0 1.0 0.0
B 0.8 0.2 0.0
C 0.333 0.333 0.333
--------
x y z
A 0.25 0.25 0.5
B 0.5 0.167 0.333
C 0.333 0.333 0.333"""

    def test_for_one_state(self):
        assert estimate_parameters(x="xyy", sigma=['x', 'y'], pi='AAA', states=['A']) == """A
A 1.0
--------
x y
A 0.333 0.667"""

    def test_for_one_character_in_alphabet_set(self):
        assert estimate_parameters(x="xxxxxxx", sigma=['x'], pi='AABBABA', states=['A', 'B']) == """A B
A 0.333 0.667
B 0.667 0.333
--------
x
A 1.0
B 1.0"""

    def test_for_unobserved_states(self):
        assert estimate_parameters(x="xxx", sigma=['x', 'y'], pi='AAA', states=['A', 'B']) == """A B
A 1.0 0.0
B 0.5 0.5
--------
x y
A 1.0 0.0
B 0.5 0.5"""

    def test_for_any_charcater_is_accepted_as_statse_or_alphabet(self):
        assert estimate_parameters(x="cfee", sigma=['c', 'e', 'f'], pi='DDXD', states=['D', 'X']) == """D X
D 0.5 0.5
X 1.0 0.0
--------
c e f
D 0.333 0.333 0.333
X 0.0 1.0 0.0"""



unittest.main(argv=[''], verbosity=2, exit=False)
