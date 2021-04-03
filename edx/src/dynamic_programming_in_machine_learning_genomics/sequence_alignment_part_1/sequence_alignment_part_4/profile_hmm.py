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

def scale_matrix(matrix, stages):
    for i, row in enumerate(matrix):
        s = sum(row)
        if s != 0:
            matrix[i] = list(map(lambda x: x/s, row))
    return  '\n'.join([' '.join([stages[i]] + list(map(str, map(lambda y: int(y) if y == 0.0 else round(y, 3), x)))) for i, x in enumerate(matrix)])

def profile_hmm(theta, sigma, alignment):
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
    # Include start state & a state that indicates insert at leadng position
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

    return ' '.join(stages) + '\n' + \
           scale_matrix(transition_matrix, stages) + '\n' + \
           '-' * 8 + '\n' + \
           ' '.join(sigma) + '\n' + \
           scale_matrix(emission_matrix, stages)

class TestProfileHMM(unittest.TestCase):
    # def test_base_case(self):
    #     print(profile_hmm(theta = 0.289,
    #                       sigma = ['A', 'B', 'C', 'D', 'E'],
    #                       alignment = ['EBA', 'E-D', 'EB-', 'EED', 'EBD', 'EBE', 'E-D', 'E-D']))

    def test_threshold_application_for_seed_alignment(self):
        sigma = ['A', 'B']
        assert profile_hmm(theta=0.4,
                           sigma=sigma,
                           alignment=['AB', 'A-']) == \
            """S I0 M1 D1 I1 E
S 0 0 1.0 0 0 0
I0 0 0 0 0 0 0
M1 0 0 0 0 0.5 0.5
D1 0 0 0 0 0 0
I1 0 0 0 0 0 1.0
E 0 0 0 0 0 0
--------
A B
S 0 0
I0 0 0
M1 1.0 0
D1 0 0
I1 0 1.0
E 0 0"""

    def test_for_correct_handling_of_deletion_states(self):
        assert profile_hmm(theta = 0.4,
                           sigma = ['A', 'B'],
                           alignment = ['A-', '-A', '-B']) == \
            """S I0 M1 D1 I1 E
S 0 0.333 0.667 0 0 0
I0 0 0 0 1.0 0 0
M1 0 0 0 0 0 1.0
D1 0 0 0 0 0 1.0
I1 0 0 0 0 0 0
E 0 0 0 0 0 0
--------
A B
S 0 0
I0 1.0 0
M1 0.5 0.5
D1 0 0
I1 0 0
E 0 0"""

    def test_for_characters_which_are_not_seen_in_multiple_alignment(self):
        assert profile_hmm(theta = 0.4,
                           sigma = ['A', 'B', 'C'],
                           alignment = ['AB', 'A-']) == \
            """S I0 M1 D1 I1 E
S 0 0 1.0 0 0 0
I0 0 0 0 0 0 0
M1 0 0 0 0 0.5 0.5
D1 0 0 0 0 0 0
I1 0 0 0 0 0 1.0
E 0 0 0 0 0 0
--------
A B C
S 0 0 0
I0 0 0 0
M1 1.0 0 0
D1 0 0 0
I1 0 1.0 0
E 0 0 0"""

    def test_basic_assignment_of_correct_states(self):
        sigma = ['A', 'B']
        assert profile_hmm(theta = 0.1,
                          sigma = ['A', 'B'],
                          alignment = ['AA', 'AA']) == \
               """S I0 M1 D1 I1 M2 D2 I2 E
S 0 0 1.0 0 0 0 0 0 0
I0 0 0 0 0 0 0 0 0 0
M1 0 0 0 0 0 1.0 0 0 0
D1 0 0 0 0 0 0 0 0 0
I1 0 0 0 0 0 0 0 0 0
M2 0 0 0 0 0 0 0 0 1.0
D2 0 0 0 0 0 0 0 0 0
I2 0 0 0 0 0 0 0 0 0
E 0 0 0 0 0 0 0 0 0
--------
A B
S 0 0
I0 0 0
M1 1.0 0
D1 0 0
I1 0 0
M2 1.0 0
D2 0 0
I2 0 0
E 0 0"""

unittest.main(argv=[''], verbosity=2, exit=False)