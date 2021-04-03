#python3
import unittest
from decimal import Decimal

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

    return transition_matrix, emission_matrix, stages, stage_to_id, alphabet_to_id

def align(x, theta, pseudocount, sigma, alignment):

    # Get transition, emission matrix and the list of states in transition graph
    transition_matrix , emission_matrix, states, state_to_id, sigma_to_id = \
        profile_hmm(theta=theta,
                    sigma=sigma,
                    alignment=alignment,
                    pseudocount=pseudocount)

    # Initialize dynamic programming matrix
    # Number of columns in the matrix is one more than emitted alphabets
    # This is because 0-th column is used to represent if initial states are
    # silent ones e.g. S->D1->D2->...
    row = [(Decimal(0), '') for _ in range(0, len(x) + 2)]
    dp = [row[0:] for _ in states[:-1]]

    dp[0][0] = (Decimal(1), '')

    # If HMM moves from initial state (S) to deletion(1) then it will not emit any symbol.
    # We are converting initial state and all deletion states to a column of silent states
    # Ref: https://www.bioinformaticsalgorithms.org/bioinformatics-chapter-10 lesson: 10.9
    # Use safari browser to read that section otherwise omages don't show up properly

    # Following section fills up 0-th column. Only non-zero values can be found corresponding to
    # deletion state (silent state)
    for current_state in states[1:]:
        if not current_state.startswith('D'):
            continue
        index = int(current_state[1:])
        prev_index = index - 1
        if prev_index >= 1:
            prev_state = 'D' + str(prev_index)
        else:
            prev_state = 'S'
        dp[state_to_id[current_state]][0] = \
            (Decimal(1 if prev_state == 'S' else dp[state_to_id[prev_state]][0][0]) *
             Decimal(transition_matrix[state_to_id[prev_state]][state_to_id[current_state]]), prev_state)

    # Process column-wise
    for i, c in enumerate(x):
        for s in states[1:-1]:
            index = int(s[1:])
            # Deletion state will be a vertical downward movement in the same column
            if s[0] == 'D':
                previous_states = ['I' + str(index - 1)] if index <= 1 else ['M' + str(index - 1), 'D' + str(index - 1), 'I' + str(index - 1)]
                previous_column = i + 1
            # For insertion / match state an alphabet will be emitted. So there is horizontal
            # movement
            elif s[0] == 'I':
                if index <= 0:
                    previous_states = ['S'] if i == 0 else ['I0']
                else:
                    previous_states = ['M' + str(index), 'D' + str(index), 'I' + str(index)]
                previous_column = i
            else:
                if index <= 1:
                    previous_states = ['S'] if i == 0 else ['I0']
                else:
                    previous_states = ['M' + str(index - 1), 'D' + str(index - 1), 'I' + str(index - 1)]
                previous_column = i

            get_max_value(emitted_char=c,
                          previous_states=previous_states,
                          previous_column=previous_column,
                          current_state=s,
                          current_column=i+1,
                          transition_matrix=transition_matrix,
                          emission_matrix=emission_matrix,
                          dp_matrix=dp,
                          sigma_to_id=sigma_to_id,
                          state_to_id=state_to_id)

    # Update the column for last slient state (end)
    for s in states[1:-1]:
        dp[state_to_id[s]][len(dp[0]) - 1] = (Decimal(dp[state_to_id[s]][len(dp[0]) - 2][0]) *
                                              Decimal(transition_matrix[state_to_id[s]][state_to_id['E']]), s)

    return ' '.join(list(reversed(backtracking(dp=dp, states=states, state_to_id=state_to_id))))

def backtracking(dp, states, state_to_id):
    max_value = float('-inf')
    backtracked_states = []
    current_state = ''
    previous_state = ''
    iteration_count = 0
    for s in reversed(states):
        if s == 'E':
            continue
        iteration_count += 1
        # Last 3 states excluding end state needs to be examined
        if iteration_count > 3:
            break
        if dp[state_to_id[s]][-1][0] > max_value:
            max_value = dp[state_to_id[s]][-1][0]
            current_state = s
            previous_state = dp[state_to_id[s]][-1][1]

    column_count = len(dp[0]) - 1

    while previous_state != 'S':
        backtracked_states.append(previous_state)
        if current_state[0] in ['I', 'M']: # Not a silent state
            column_count = column_count - 1 # Move to previous column
        current_state = previous_state
        previous_state = dp[state_to_id[current_state]][column_count][1]
    return backtracked_states

# Determines the maximum value from all predecessor states.
# Once the value of the current state is computed it is stored
# as tuple (value, previous state)
# Tuple structure helps figuring out the previous state during
# backtracking
def get_max_value(emitted_char,
                  previous_states,
                  previous_column,
                  current_state,
                  current_column,
                  transition_matrix,
                  emission_matrix,
                  dp_matrix,
                  state_to_id,
                  sigma_to_id):

    max_value = float('-inf')
    max_prev_state = ''
    for p in previous_states:
        value = Decimal(transition_matrix[state_to_id[p]][state_to_id[current_state]]) * Decimal(dp_matrix[state_to_id[p]][previous_column][0])
        if value > max_value:
            max_value = value
            max_prev_state = p
    dp_matrix[state_to_id[current_state]][current_column] = (Decimal(emission_matrix[state_to_id[current_state]][sigma_to_id[emitted_char]] if not current_state.startswith('D') else 1.0) * max_value, max_prev_state)

def print_matrix(matrix, significant_digits=6):
    for r in matrix:
        print(' '.join([str(x[0]) + ',' + x[1] if isinstance(x, tuple) else str(x) for x in r]))

class TestProfileHMMPseudocount(unittest.TestCase):

    def test_base_case(self):
        assert align(x="AEFDFDC",
                     theta=0.4,
                     pseudocount=.01,
                     sigma =['A', 'B', 'C', 'D', 'E', 'F'],
                     alignment =['ACDEFACADF',
                                 'AFDA---CCF',
                                 'A--EFD-FDC',
                                 'ACAEF--A-C',
                                 'ADDEFAAADF']) == 'M1 D2 D3 M4 M5 I5 M6 M7 M8'

    def test_for_deletion_states_in_the_beginning(self):
        assert align(x="B",
                     theta=0.4,
                     pseudocount=.01,
                     sigma=['A', 'B'],
                     alignment=['AAAB', 'AAAB', '---B']) == 'D1 D2 D3 M4'

    def test_for_correct_handling_of_deletion_states(self):
        assert align(x="AB",
                     theta=0.4,
                     pseudocount=.01, sigma=['A', 'B'],
                     alignment=['AAAAB', 'AAAAB']) in ['M1 D2 D3 D4 M5', 'D1 D2 D3 M4 M5']

    def test_for_contiguous_run_of_insertion(self):
        assert align(x="AAAAAB",
                     theta=0.4,
                     pseudocount=0.01,
                     sigma=['A', 'B'],
                     alignment=['-B', '-B']) == 'I0 I0 I0 I0 I0 M1'

    def test_states_for_matches_and_mismatches(self):
        assert align(x="AB",
                     theta=0.4,
                     pseudocount=.01,
                     sigma=['A', 'B'],
                     alignment=['AA', 'AA']) == 'M1 M2'

    def test_for_unused_alphabet(self):
        assert align(x='AB',
                     theta=0.4,
                     pseudocount=0.01,
                     sigma=['A', 'B', 'C', 'D', 'E'],
                     alignment=['AA', 'AA']) == 'M1 M2'

    def test_for_correct_transition_to_insertion_state(self):
        assert align(x='AB',
                     theta=0.4,
                     pseudocount=0.01,
                     sigma=['A', 'B'],
                     alignment=['A-', 'A-']) == 'M1 I1'

unittest.main(argv=[''], verbosity=2, exit=False)
