import unittest
from cppalgorithm import (
    sort, stable_sort, is_sorted,
    lower_bound, upper_bound, binary_search
)

class TestSorting(unittest.TestCase):
    def test_sort(self):
        data = [5, 2, 8, 1, 9]
        sort(data)
        self.assertEqual(data, [1, 2, 5, 8, 9])
        self.assertTrue(is_sorted(data))

    def test_sort_reverse(self):
        data = [1, 5, 2]
        sort(data, reverse=True)
        self.assertEqual(data, [5, 2, 1])

    def test_stable(self):
        # Sort by length
        data = ["apple", "bat", "cat", "ant"]
        stable_sort(data, key=len)
        self.assertEqual(data, ["bat", "cat", "ant", "apple"])
        # 'bat' came before 'cat' and 'ant' in original, should strictly preserve relative order

    def test_binary_search(self):
        data = [1, 2, 4, 4, 4, 6, 7]
        self.assertTrue(binary_search(data, 4))
        self.assertFalse(binary_search(data, 5))
        self.assertFalse(binary_search(data, 99))

    def test_bounds(self):
        data = [10, 20, 20, 20, 30]
        # lower_bound(20) -> first 20 -> index 1
        self.assertEqual(lower_bound(data, 20), 1)
        # upper_bound(20) -> first element > 20 -> index 4 (30)
        self.assertEqual(upper_bound(data, 20), 4)

if __name__ == '__main__':
    unittest.main()
