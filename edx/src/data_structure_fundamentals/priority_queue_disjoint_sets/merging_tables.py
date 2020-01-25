import unittest
import random

class Database:
    def __init__(self, row_counts):
        self.row_counts = row_counts[0:]
        self.max_row_count = max(row_counts)
        n_tables = len(row_counts)
        self.ranks = [1] * n_tables
        self.parents = list(range(n_tables))

    def find_brute_force(self, node):
        while node != self.parents[node]:
            node = self.parents[node]
        return self.parents[node]

    def merge_brute_force(self, src, dst):
        src_parent = self.find_brute_force(src)
        dst_parent = self.find_brute_force(dst)
        if src_parent != dst_parent:
            self.parents[src_parent] = dst_parent
            self.row_counts[dst_parent] += self.row_counts[src_parent]
            self.max_row_count = max(self.max_row_count, self.row_counts[dst_parent])

    def merge(self, src, dst):
        src_parent = self.get_parent(src)
        dst_parent = self.get_parent(dst)

        if src_parent == dst_parent:
            return False
        if self.ranks[src_parent] > self.ranks[dst_parent]:
            self.parents[dst_parent] = src_parent
            self.row_counts[src_parent] += self.row_counts[dst_parent]
            self.max_row_count = max(self.row_counts[src_parent], self.max_row_count)
        else:
            self.parents[src_parent] = dst_parent
            self.row_counts[dst_parent] += self.row_counts[src_parent]
            self.max_row_count = max(self.row_counts[dst_parent], self.max_row_count)
            if self.ranks[src_parent] == self.ranks[dst_parent]:
                self.ranks[dst_parent] += 1
        # merge two components
        # use union by rank heuristic
        # update max_row_count with the new maximum table size
        return True

    def get_parent(self, table):
        # find parent and compress path
        if self.parents[table] != table:
            table = self.get_parent(self.parents[table])
        return self.parents[table]

def main():
    n_tables, n_queries = map(int, input().split())
    counts = list(map(int, input().split()))
    assert len(counts) == n_tables
    db = Database(counts)
    for i in range(n_queries):
        dst, src = map(int, input().split())
        db.merge(dst - 1, src - 1)
        print(db.max_row_count)

if __name__ == '__main__':
    main()

class TestDatabase(unittest.TestCase):

    def _execute_test(self, counts, queries):
        test_db = Database(counts)
        db = Database(counts)
        expected = []
        actual = []
        for i in range(len(queries)):
            dst, src = queries[i]
            test_db.merge_brute_force(dst - 1, src - 1)
            expected.append(test_db.max_row_count)
        for i in range(len(queries)):
            dst, src = queries[i]
            db.merge(dst - 1, src - 1)
            actual.append(db.max_row_count)
        self.assertEqual(expected, actual)

    def test_first_scenario_from_problem_statement(self):
        counts = [1, 1, 1, 1, 1]
        queries = [(3, 5), (2, 4), (1, 4), (5, 4), (5, 3)]
        self._execute_test(counts, queries)

    def test_second_scenario_from_problem_statement(self):
        counts = [10, 0, 5, 0, 3, 3]
        queries = [(6, 6), (6, 5), (5, 4), (4, 3)]
        self._execute_test(counts, queries)

    def test_third_scenario_from_problem_statement(self):
        counts = [6, 2, 6, 9]
        queries = [(1, 4), (2, 3), (3, 1), (3, 1), (2, 4)]
        self._execute_test(counts, queries)

    def test_with_random_data(self):
        # Repeat with random data for 100 times
        for i in range(0, 100):
            n_tables, n_queries = (random.randint(1, 20), random.randint(1, 20))
            counts = [random.randint(1, 10) for i in range(0, n_tables)]
            queries = [(random.randint(1, n_tables), random.randint(1, n_tables)) for i in range(0, n_queries)]
            self._execute_test(counts, queries)

# if __name__ == '__main__':
#     unittest.main(argv=[''], verbosity=2, exit=False)
#    main()