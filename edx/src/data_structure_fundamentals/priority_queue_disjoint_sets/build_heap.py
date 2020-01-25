import math
import unittest

def parent(i):
    return int(math.floor((i - 1) / 2))

def left_chid(i):
    return 2 * i + 1

def right_child(i):
    return 2 * i + 2

def sift_down(i, data, swaps):
    min_index = i
    lchild_index = left_chid(i)
    if lchild_index < len(data) and data[min_index] > data[lchild_index]:
        min_index = lchild_index
    rchild_index = right_child(i)
    if rchild_index < len(data) and data[min_index] > data[rchild_index]:
        min_index = rchild_index
    if i != min_index:
        swaps.append((i, min_index))
        data[i], data[min_index] = data[min_index], data[i]
        sift_down(min_index, data, swaps)

def build_heap(data):
    n = len(data)
    swaps = []
    for i in range(math.floor(n / 2), -1, -1):
        sift_down(i, data, swaps)
    return(swaps)

def main():
    n = int(input())
    data = list(map(int, input().split()))
    assert len(data) == n
    swaps = build_heap(data)
    print(len(swaps))
    for i, j in swaps:
        print(i, j)

class TestBuildHeap(unittest.TestCase):
    def test_build_heap_with_odd_number_of_unique_elements(self):
        data = [10, 11, 7, 2, 1, 13, 14, 21, 9]
        swaps = build_heap(data)
        self.assertEqual(len(swaps), 4)
        self.assertEqual(swaps, [(1, 4), (0, 1), (1, 3), (3, 8)])

    def test_build_heap_with_even_number_of_unique_elements(self):
        data = [10, 5, 9 , 7, 11, 12]
        swaps = build_heap(data)
        self.assertEqual(len(swaps), 2)
        self.assertEqual(swaps, [(0, 1), (1, 3)])

unittest.main(argv=[''], verbosity=2, exit=False)
