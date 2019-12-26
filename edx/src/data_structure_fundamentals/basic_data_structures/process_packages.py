from collections import namedtuple
import unittest

Request = namedtuple("Request", ["arrived_at", "time_to_process", "started_at"], defaults=(None,) * 3)
Response = namedtuple("Response", ["was_dropped", "started_at"])


class Buffer:
    def __init__(self, capacity):
        self.capacity = capacity
        self.queue = [None] * capacity
        self.head = 0
        self.tail = 0
        self.size = 0

    def peek(self):
        if self.size > 0:
            return self.queue[self.head]
        else:
            return None

    def add(self, index):
        if self.size < self.capacity:
            self.size += 1
            self.queue[self.tail] = index
            self.tail = (self.tail + 1) % self.capacity
        else:
            response = Response(True, -1)
            return response
        return None

    def remove(self):
        self.size -= 1
        index = self.queue[self.head]
        self.queue[self.head] = None
        self.head = (self.head + 1) % self.capacity
        return index

def process_requests(requests, buffer):
    responses = [None] * len(requests)
    elapsed_time = 0 if len(requests) == 0 else requests[0].arrived_at
    processing = False
    for index, request in enumerate(requests):
        # Before queuing the request make sure that the one that was processed has completed and discard it
        if processing:
            peeked_request = buffer.peek()
            if requests[index].arrived_at >= (requests[peeked_request].started_at + requests[peeked_request].time_to_process):
                processing = False
                request_index = buffer.remove()
                responses[request_index] = Response(False, requests[request_index].started_at)
        # Attempt to add request to queue
        response = buffer.add(index)
        # If queue is full already then return non-null response object
        if response is not None:
            responses[index] = response
        else:
            processing = True
            requests[index] = Request(request.arrived_at, request.time_to_process, max(elapsed_time, request.arrived_at))
            elapsed_time += request.time_to_process
    for i in range(0, buffer.size):
        request_index = buffer.remove()
        responses[request_index] = Response(False, requests[request_index].started_at)
    return responses

def main():
    buffer_size = 1
    requests = [Request(0, 1), Request(2, 1)]
    buffer = Buffer(buffer_size)
    print(process_requests(requests, buffer))

class TestProcessRequests(unittest.TestCase):
    def test_buffer_size_2_with_4_nonoverlapping_requests(self):
        responses = process_requests([Request(0, 1), Request(2, 3), Request(5, 2), Request(9, 3)], Buffer(2))
        self.assertEqual([0, 2, 5, 9], [r.started_at for r in responses])

    def test_buffer_size_1_with_4_nonoverlapping_requests(self):
        responses = process_requests([Request(0, 1), Request(2, 3), Request(5, 2), Request(9, 3)], Buffer(1))
        self.assertEqual([0, 2, 5, 9], [r.started_at for r in responses])

    def test_buffer_size_1_with_first_two_requests_having_same_arrival_time(self):
        responses = process_requests([Request(0, 1), Request(0, 3), Request(5, 2), Request(9, 3)], Buffer(1))
        self.assertEqual([0, -1, 5, 9], [r.started_at for r in responses])

    def test_buffer_size_2_with_first_two_requests_having_same_arrival_time(self):
        responses = process_requests([Request(0, 1), Request(0, 3), Request(5, 2), Request(9, 3)], Buffer(2))
        self.assertEqual([0, 1, 5, 9], [r.started_at for r in responses])

    def test_buffer_size_2_with_first_three_overlapping_arrival_times(self):
        responses = process_requests([Request(0, 3), Request(1, 2), Request(2, 1), Request(9, 3)], Buffer(2))
        self.assertEqual([0, 3, -1, 9], [r.started_at for r in responses])

    def test_buffer_size_1_with_first_three_overlapping_arrival_times(self):
        responses = process_requests([Request(0, 3), Request(1, 2), Request(2, 1), Request(9, 3)], Buffer(1))
        self.assertEqual([0, -1, -1, 9], [r.started_at for r in responses])

    def test_buffer_size_2_with_first_two_requests_following_each_other(self):
        responses = process_requests([Request(0, 3), Request(3, 2), Request(6, 1), Request(9, 3)], Buffer(2))
        self.assertEqual([0, 3, 6, 9], [r.started_at for r in responses])

    def test_buffer_size_1_with_first_two_requests_following_each_other(self):
        responses = process_requests([Request(0, 3), Request(3, 2), Request(6, 1), Request(9, 3)], Buffer(1))
        self.assertEqual([0, 3, 6, 9], [r.started_at for r in responses])

    def test_buffer_size_2_with_first_and_last_two_requests_overlapping(self):
        responses = process_requests([Request(0, 3), Request(2, 3), Request(6, 4), Request(9, 3)], Buffer(2))
        self.assertEqual([0, 3, 6, 10], [r.started_at for r in responses])

    def test_buffer_size_1_with_first_and_last_two_requests_overlapping(self):
        responses = process_requests([Request(0, 3), Request(2, 3), Request(6, 4), Request(9, 3)], Buffer(1))
        self.assertEqual([0, -1, 6, -1], [r.started_at for r in responses])

unittest.main(argv=[''], verbosity=2, exit=False)