import math
import unittest
from collections import namedtuple
import random

AssignedJob = namedtuple("AssignedJob", ["thread_id", "started_at", "processing_time", "ended_at"])

class node:
    def __init__(self, id, value):
        self.id = id
        self.value = value

class Heap:
    def __init__(self, data):
        self.data = data
        self.size = len(data)

    def __str__(self):
        return ','.join([str(d.id) +  ':' + str(d.value) for d in self.data])

    def parent(self, i):
        return int(math.floor((i - 1) / 2))

    def left_child(self, i):
        return 2 * i + 1

    def right_child(self, i):
        return 2 * i + 2

    def build_heap(self):
        for i in range(math.floor(self.size / 2) - 1, -1, -1):
            self._sift_down(i)

    def peek(self):
        if self.size > 0:
            return self.data[0]
        else:
            None

    def insert(self, n):
        if self.size < len(self.data):
            self.data[self.size] = n
        else:
            self.data.append(n)
        self.size += 1
        self._sift_up(self.size - 1)

    def _compare(self, node1, node2):
        if node1.value > node2.value:
            return True
        elif node1.value == node2.value and node1.id > node2.id:
            return True
        return False

    def _sift_up(self, i):
        parent_index = int(math.floor((i - 1) / 2))
        if parent_index >= 0 and self._compare(self.data[parent_index], self.data[i]):
            self.data[parent_index], self.data[i] = self.data[i], self.data[parent_index]
            self._sift_up(parent_index)

    def _sift_down(self, i):
        min_index = i
        left_index = self.left_child(i)
        if left_index < self.size and self._compare(self.data[min_index], self.data[left_index]):
            min_index = left_index
        right_index = self.right_child(i)
        if right_index < self.size and self._compare(self.data[min_index], self.data[right_index]):
            min_index = right_index
        if min_index != i:
            self.data[min_index], self.data[i] = self.data[i], self.data[min_index]
            self._sift_down(min_index)

    def extract_min(self):
        min_value = None
        if self.size > 0:
            min_value = self.data[0]
            self.data[0], self.data[self.size - 1] = self.data[self.size - 1], self.data[0]
            self.size -= 1
            self._sift_down(0)
        return(min_value)

class TestHeap(unittest.TestCase):
    def _setup_heap_with_odd_number_element_count(self):
        test_heap = Heap([node(index, i) for index, i in enumerate([5, 4, 3, 2, 1])])
        test_heap.build_heap()
        return test_heap

    def _setup_heap_with_even_number_element_count(self):
        test_heap = Heap([node(index, i) for index, i in enumerate([13, 11, 17, 19, 20, 7])])
        test_heap.build_heap()
        return test_heap

    def _setup_heap_with_nonunique_elements(self):
        test_heap = Heap([node(index, i) for index, i in enumerate([0, 0, 3, 2, 4])])
        test_heap.build_heap()
        return test_heap

    def test_build_heap_with_nonunique_elements(self):
        test_heap = self._setup_heap_with_nonunique_elements()
        self.assertEqual(test_heap.size, 5)

    def test_build_heap_with_odd_number_element_count(self):
        test_heap = self._setup_heap_with_odd_number_element_count()
        self.assertEqual(test_heap.size, 5)
        self.assertEqual([d.id for d in test_heap.data], [4, 3, 2, 0, 1])
        self.assertEqual([d.value for d in test_heap.data], [1, 2, 3, 5, 4])

    def test_build_heap_with_even_number_element_count(self):
        test_heap = self._setup_heap_with_even_number_element_count()
        self.assertEqual(test_heap.size, 6)
        self.assertEqual([d.value for d in test_heap.data], [7, 11, 13, 19, 20, 17])
        self.assertEqual([d.id for d in test_heap.data], [5, 1, 0, 3, 4, 2])

    def test_extract_min_from_heap_with_odd_number_element_count(self):
        test_heap = self._setup_heap_with_odd_number_element_count()
        self.assertEqual(test_heap.size, 5)
        node = test_heap.extract_min()
        self.assertEqual(test_heap.size, 4)
        self.assertEqual(node.value, 1)
        self.assertEqual(test_heap.peek().value, 2)

    def test_extract_min_from_heap_with_even_number_element_count(self):
        test_heap = self._setup_heap_with_even_number_element_count()
        self.assertEqual(test_heap.size, 6)
        node = test_heap.extract_min()
        self.assertEqual(test_heap.size, 5)
        self.assertEqual(node.value, 7)
        self.assertEqual(test_heap.peek().value, 11)

    def test_insert_into_heap_with_odd_number_element_count(self):
        test_heap = self._setup_heap_with_odd_number_element_count()
        self.assertEqual(test_heap.size, 5)
        test_heap.extract_min()
        self.assertEqual(test_heap.size, 4)
        test_heap.insert(node(0, 7))
        test_heap.insert(node(6, 0))
        self.assertEqual([d.value for d in test_heap.data], [0, 4, 2, 5, 7, 3])

    def test_insert_into_heap_with_even_number_element_count(self):
        test_heap = self._setup_heap_with_even_number_element_count()
        self.assertEqual(test_heap.size, 6)
        test_heap.insert(node(6, 14))
        test_heap.insert(node(7, 0))
        self.assertEqual([d.value for d in test_heap.data], [0, 7, 13, 11, 20, 17, 14, 19])

class ParallelProcess:
    def __init__(self, thread_pool_size, jobs):
        self.jobs = jobs
        self.thread_pool_size = thread_pool_size
        self.job_thread_map = {}
        self.threads_heap = Heap([node(i, 0) for i in range(0,self.thread_pool_size)])
        self.threads_heap.build_heap()

    def _mark_completed_job(self):
        completed_job = self.jobs_heap.extract_min()
        job_entry = self.job_thread_map[completed_job.id]
        self.job_thread_map[completed_job.id] = AssignedJob(job_entry.thread_id, job_entry.started_at, job_entry.processing_time, job_entry.started_at + job_entry.processing_time)
        self.threads_heap.insert(job_entry.thread_id, job_entry.thread_id)

    def process_jobs(self):
        for job_index in range(0, len(self.jobs)):
            available_thread = self.threads_heap.extract_min()
            self.job_thread_map[job_index] = AssignedJob(available_thread.id, available_thread.value, self.jobs[job_index], available_thread.value + self.jobs[job_index])
            available_thread.value += self.jobs[job_index]
            self.threads_heap.insert(available_thread)
        return [(self.job_thread_map[k].thread_id, self.job_thread_map[k].started_at) for k in sorted(self.job_thread_map.keys())]

    def assign_jobs(self):
    # Brute force algorithm
        result = []
        next_free_time = [0] * self.thread_pool_size
        for job in self.jobs:
            next_worker = min(range(self.thread_pool_size), key=lambda w: next_free_time[w])
            result.append(AssignedJob(next_worker, next_free_time[next_worker], job, next_free_time[next_worker] + job))
            next_free_time[next_worker] += job
        return result

class TestParallelProcess(unittest.TestCase):

    def _compare_actual_expected(self, actual, expected):
        self.assertEqual(len(expected), len(actual))
        for i in range(0, len(expected)):
            self.assertEqual(expected[i].thread_id, actual[i][0])
            self.assertEqual(expected[i].started_at, actual[i][1])

    def test_parallel_process_with_non_unique_processing_time_and_two_threads(self):
        parallel_process = ParallelProcess(2, [0, 0, 1, 2])
        expected = parallel_process.assign_jobs()
        actual = parallel_process.process_jobs()
        self._compare_actual_expected(actual, expected)

    def test_parallel_process_with_strict_descending_order_processing_time_and_two_threads(self):
        parallel_process = ParallelProcess(2, [5, 4, 3, 2, 1])
        expected = parallel_process.assign_jobs()
        actual = parallel_process.process_jobs()
        self._compare_actual_expected(actual, expected)

    def test_parallel_process_with_strict_descending_order_processing_time_and_three_threads(self):
        parallel_process = ParallelProcess(3, [5, 4, 3, 2, 1])
        expected = parallel_process.assign_jobs()
        actual = parallel_process.process_jobs()
        self._compare_actual_expected(actual, expected)

    def test_parallel_process_with_three_competing_threads(self):
        parallel_process = ParallelProcess(3, [5, 4, 3, 2, 1, 8])
        expected = parallel_process.assign_jobs()
        actual = parallel_process.process_jobs()
        self._compare_actual_expected(actual, expected)

    def test_parallel_process_with_more_than_one_scenario_for_competing_threads(self):
        parallel_process = ParallelProcess(3, [5, 4, 3, 2, 1, 8, 6])
        expected = parallel_process.assign_jobs()
        actual = parallel_process.process_jobs()
        self._compare_actual_expected(actual, expected)

    def test_parallel_process_jobs_with_same_processing_time_and_four_threads(self):
        parallel_process = ParallelProcess(4, [1] * 20)
        expected = parallel_process.assign_jobs()
        actual = parallel_process.process_jobs()
        self._compare_actual_expected(actual, expected)

    def test_parallel_process_with_fifty_randomly_generated_job_time_and_ten_threads(self):
        jobs = [random.randint(0,10) for i in range(0,50)]
        parallel_process = ParallelProcess(10, jobs)
        expected = parallel_process.assign_jobs()
        actual = parallel_process.process_jobs()
        self._compare_actual_expected(actual, expected)

if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)

