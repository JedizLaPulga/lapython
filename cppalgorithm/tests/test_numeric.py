import unittest
from cppalgorithm import (
    iota, accumulate, inner_product,
    partial_sum, adjacent_difference
)

class TestNumeric(unittest.TestCase):
    def test_iota(self):
        data = [0]*5
        iota(data, 10)
        self.assertEqual(data, [10, 11, 12, 13, 14])

    def test_accumulate(self):
        data = [1, 2, 3, 4]
        res = accumulate(data, 0)
        self.assertEqual(res, 10)
        
        # Product
        res_prod = accumulate(data, 1, lambda x, y: x * y)
        self.assertEqual(res_prod, 24)

    def test_inner_product(self):
        a = [1, 2, 3]
        b = [2, 3, 4]
        # (1*2) + (2*3) + (3*4) = 2 + 6 + 12 = 20
        res = inner_product(a, b, 0)
        self.assertEqual(res, 20)

    def test_partial_sum(self):
        data = [1, 2, 3, 4]
        dest = []
        partial_sum(data, dest.append)
        self.assertEqual(dest, [1, 3, 6, 10])

    def test_adjacent_difference(self):
        data = [1, 3, 6, 10]
        dest = []
        adjacent_difference(data, dest.append)
        self.assertEqual(dest, [1, 2, 3, 4])

if __name__ == '__main__':
    unittest.main()
