#python3
import sys
import unittest

def build_transition_graph(stages, match_stages):
    transition = {}
    for s in stages:
        if s == 'E':
            continue
        if s.startswith('I'):
            transition[s] = [s]
        elif s == 'S':
            transition[s] = ['D1', 'M1', 'I0']
        else:
            if s[0] in ['D', 'M'] and int(s[1:]) >= 2:
                transition[s[0] + str(int(s[1:]) - 1)].append(s)
                transition[s] = []
                if s[0] == 'D':
                    transition['M' + str(int(s[1:]) - 1)].append(s)
                if s[0] == 'M':
                    transition['D' + str(int(s[1:]) - 1)].append(s)
            else:
                transition[s] = []

    for i in range(1, match_stages + 1):
        for s in ['D', 'M']:
            transition[s + str(i)].append('I' + str(i))
        if i == 1:
            transition['I0'].extend(['D1', 'M1'])
        if i + 1 <= match_stages:
            transition['I' + str(i)].extend(['D' + str(i + 1), 'M' + str(i + 1)])
        else:
            for f in ['D', 'M', 'I']:
                transition[f + str(i)].append('E')
    return transition

def apply_pseudocount_to_transition_matrix(transition_matrix, transition_graph, stage_to_id, pseudocount):
    scale_matrix(transition_matrix)
    for i in transition_graph.keys():
        sum_allowed_transitions =  sum([transition_matrix[stage_to_id[i]][stage_to_id[j]] for j in transition_graph[i]])
        if sum_allowed_transitions == 0:
            for j in transition_graph[i]:
                transition_matrix[stage_to_id[i]][stage_to_id[j]] = 1.0 / len(transition_graph[i])
        else:
            for j in transition_graph[i]:
                transition_matrix[stage_to_id[i]][stage_to_id[j]] = \
                    (transition_matrix[stage_to_id[i]][stage_to_id[j]] + pseudocount) \
                          / (1.0 + pseudocount * len(transition_graph[i]))

def apply_pseudocount_to_emission_matrix(emission_matrix, stage_to_id, alphabet_to_id, pseudocount):
    scale_matrix(emission_matrix)
    for i in stage_to_id.keys():
        if i in ['S', 'E'] or i.startswith('D'):
            continue
        sum_allowed_emissions =  sum(emission_matrix[stage_to_id[i]])
        if sum_allowed_emissions == 0:
            for j in alphabet_to_id.values():
                emission_matrix[stage_to_id[i]][j] = 1.0 / len(alphabet_to_id.keys())
        else:
            for j in alphabet_to_id.values():
                emission_matrix[stage_to_id[i]][j] = \
                    (emission_matrix[stage_to_id[i]][j] + pseudocount) \
                    / (1.0 + pseudocount * len(alphabet_to_id.keys()))

def scale_matrix(matrix):
    for i, row in enumerate(matrix):
        s = sum(row)
        if s != 0:
            matrix[i] = list(map(lambda x: x/s, row))

def matrix_to_str(matrix, stages):
    return  '\n'.join([' '.join([stages[i]] + list(map(str, map(lambda y: int(y) if y == 0.0 else round(y, 5), x)))) for i, x in enumerate(matrix)])

def profile_hmm(theta, sigma, alignment, pseudocount):
    match_stages = []
    # Find out how many match stages will be there
    # It will depend on which match stages need to be eliminated based on theta
    for j in range(0, len(alignment[0])):
        skip_count = 0
        total_count = 0
        for i in range(0, len(alignment)):
            if alignment[i][j] == '-':
                skip_count += 1
            total_count += 1
        if float(skip_count) / float(total_count) < theta:
            match_stages.append(1)
        else:
            match_stages.append(0)
    # Generate a list of all stages in HMM
    # Include start state & a state that indicates insert at leading position
    stages = ['S', 'I0']
    for k in range(sum(match_stages)):
        # Add equal number of match, delete and insert states
        stages.extend(['M' + str(k + 1), 'D' + str(k + 1), 'I' + str(k + 1)])
    # End state
    stages.append('E')

    # Dict to convert alphanumeric state to number
    stage_to_id = {}
    for i, s in enumerate(stages):
        stage_to_id[s] = i

    # Dict to convert alphabet to number
    alphabet_to_id = {}
    for i, s in enumerate(sigma):
        alphabet_to_id[s] = i

    transition_graph = build_transition_graph(stages, sum(match_stages))

    row = [0 for _ in stages]
    transition_matrix = [row[0:] for _ in stages]
    row = [0 for _ in sigma]
    emission_matrix = [row[0:] for _ in stages]

    for alignment_str in alignment:
        current_state = 'S'
        for i, s in enumerate(alignment_str):
            if match_stages[i] == 1:
                next_state = [x for x in transition_graph[current_state] if x.startswith('M' if s != '-' else 'D')][0]
                if s != '-':
                    emission_matrix[stage_to_id[next_state]][alphabet_to_id[s]] += 1
            else:
                if s != '-':
                    next_state = [x for x in transition_graph[current_state] if x.startswith('I')][0]
                    emission_matrix[stage_to_id[next_state]][alphabet_to_id[s]] += 1
                else:
                    continue
            transition_matrix[stage_to_id[current_state]][stage_to_id[next_state]] += 1

            current_state = next_state
        transition_matrix[stage_to_id[current_state]][stage_to_id['E']] = 1

    apply_pseudocount_to_transition_matrix(transition_matrix, transition_graph, stage_to_id, pseudocount)

    apply_pseudocount_to_emission_matrix(emission_matrix, stage_to_id, alphabet_to_id, pseudocount)

    return ' '.join(stages) + '\n' + \
           matrix_to_str(transition_matrix, stages) + '\n' + \
           '-' * 8 + '\n' + \
           ' '.join(sigma) + '\n' + \
           matrix_to_str(emission_matrix, stages)

class TestProfileHMMPseudocount(unittest.TestCase):

    def test_base_case(self):
        assert profile_hmm(theta=0.289,
                           pseudocount=.01,
                           sigma =['A', 'B', 'C', 'D', 'E'],
                           alignment =['EBA', 'E-D', 'EB-', 'EED', 'EBD', 'EBE', 'E-D', 'E-D']) == \
               """S I0 M1 D1 I1 M2 D2 I2 E
S 0 0.00971 0.98058 0.00971 0 0 0 0 0
I0 0 0.33333 0.33333 0.33333 0 0 0 0 0
M1 0 0 0 0 0.6165 0.37379 0.00971 0 0
D1 0 0 0 0 0.33333 0.33333 0.33333 0 0
I1 0 0 0 0 0.00971 0.78641 0.20388 0 0
M2 0 0 0 0 0 0 0 0.0098 0.9902
D2 0 0 0 0 0 0 0 0.0098 0.9902
I2 0 0 0 0 0 0 0 0.5 0.5
E 0 0 0 0 0 0 0 0 0
--------
A B C D E
S 0 0 0 0 0
I0 0.2 0.2 0.2 0.2 0.2
M1 0.00952 0.00952 0.00952 0.00952 0.9619
D1 0 0 0 0 0
I1 0.00952 0.77143 0.00952 0.00952 0.2
M2 0.14558 0.00952 0.00952 0.6898 0.14558
D2 0 0 0 0 0
I2 0.2 0.2 0.2 0.2 0.2
E 0 0 0 0 0"""

    def test_pseudocount_getting_applied_corrrectly_for_single_char_string(self):
        assert profile_hmm(theta=0.1,
                           pseudocount=.01,
                           sigma =['A'],
                           alignment =['A']) == \
        """S I0 M1 D1 I1 E
S 0 0.00971 0.98058 0.00971 0 0
I0 0 0.33333 0.33333 0.33333 0 0
M1 0 0 0 0 0.0098 0.9902
D1 0 0 0 0 0.5 0.5
I1 0 0 0 0 0.5 0.5
E 0 0 0 0 0 0
--------
A
S 0
I0 1.0
M1 1.0
D1 0
I1 1.0
E 0"""

    def test_pseudocount_getting_applied_corrrectly_for_multicharacter_alphabet(self):
        assert profile_hmm(theta=0.1,
                           pseudocount=.01,
                           sigma =['A', 'B'],
                           alignment =['A']) == \
               """S I0 M1 D1 I1 E
S 0 0.00971 0.98058 0.00971 0 0
I0 0 0.33333 0.33333 0.33333 0 0
M1 0 0 0 0 0.0098 0.9902
D1 0 0 0 0 0.5 0.5
I1 0 0 0 0 0.5 0.5
E 0 0 0 0 0 0
--------
A B
S 0 0
I0 0.5 0.5
M1 0.9902 0.0098
D1 0 0
I1 0.5 0.5
E 0 0"""

    def test_pseudocount_is_getting_applied_correctly(self):
        assert profile_hmm(theta=0.1,
                           pseudocount=.01,
                           sigma =['A', 'B'],
                           alignment =['A']) == \
               """S I0 M1 D1 I1 E
S 0 0.00971 0.98058 0.00971 0 0
I0 0 0.33333 0.33333 0.33333 0 0
M1 0 0 0 0 0.0098 0.9902
D1 0 0 0 0 0.5 0.5
I1 0 0 0 0 0.5 0.5
E 0 0 0 0 0 0
--------
A B
S 0 0
I0 0.5 0.5
M1 0.9902 0.0098
D1 0 0
I1 0.5 0.5
E 0 0"""

    def test_threshold_is_getting_applied_correctly(self):
        assert profile_hmm(theta=0.4,
                           pseudocount=.01,
                           sigma =['A', 'B'],
                           alignment =['AB', 'A-']) == \
            """S I0 M1 D1 I1 E
S 0 0.00971 0.98058 0.00971 0 0
I0 0 0.33333 0.33333 0.33333 0 0
M1 0 0 0 0 0.5 0.5
D1 0 0 0 0 0.5 0.5
I1 0 0 0 0 0.0098 0.9902
E 0 0 0 0 0 0
--------
A B
S 0 0
I0 0.5 0.5
M1 0.9902 0.0098
D1 0 0
I1 0.0098 0.9902
E 0 0"""

    def test_deletion_state_is_handled_correctly(self):
        assert profile_hmm(theta=0.4,
                           pseudocount=.01,
                           sigma =['A', 'B'],
                           alignment =['A-', '-A', '-B']) == \
            """S I0 M1 D1 I1 E
S 0 0.33333 0.65696 0.00971 0 0
I0 0 0.00971 0.00971 0.98058 0 0
M1 0 0 0 0 0.0098 0.9902
D1 0 0 0 0 0.0098 0.9902
I1 0 0 0 0 0.5 0.5
E 0 0 0 0 0 0
--------
A B
S 0 0
I0 0.9902 0.0098
M1 0.5 0.5
D1 0 0
I1 0.5 0.5
E 0 0"""

    def test_insertion_state_allows_transition_to_itself(self):
        assert profile_hmm(theta=0.5,
                           pseudocount=.01,
                           sigma =['A', 'B'],
                           alignment =['AA-', '--A', '--B']) == \
            """S I0 M1 D1 I1 E
S 0 0.33333 0.65696 0.00971 0 0
I0 0 0.49515 0.00971 0.49515 0 0
M1 0 0 0 0 0.0098 0.9902
D1 0 0 0 0 0.0098 0.9902
I1 0 0 0 0 0.5 0.5
E 0 0 0 0 0 0
--------
A B
S 0 0
I0 0.9902 0.0098
M1 0.5 0.5
D1 0 0
I1 0.5 0.5
E 0 0"""


unittest.main(argv=[''], verbosity=2, exit=False)