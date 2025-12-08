import unittest
from cppalgorithm import (
    merge, includes,
    set_union, set_intersection,
    set_difference, set_symmetric_difference
)

class TestSetOperations(unittest.TestCase):
    def test_merge(self):
        a = [1, 3, 5]
        b = [2, 4, 6]
        res = []
        merge(a, b, res.append)
        self.assertEqual(res, [1, 2, 3, 4, 5, 6])
        
    def test_includes(self):
        a = [1, 2, 3, 4, 5]
        b = [1, 3, 5]
        self.assertTrue(includes(a, b))
        
        c = [1, 6]
        self.assertFalse(includes(a, c))

    def test_set_union(self):
        a = [1, 2, 3]
        b = [3, 4, 5]
        res = []
        set_union(a, b, res.append)
        # 1, 2, 3, 4, 5 (3 is common, included once)
        self.assertEqual(res, [1, 2, 3, 4, 5])

    def test_set_intersection(self):
        a = [1, 2, 3, 10]
        b = [3, 4, 5, 10]
        res = []
        set_intersection(a, b, res.append)
        self.assertEqual(res, [3, 10])

    def test_set_difference(self):
        # elements in A but not in B
        a = [1, 2, 3, 4, 5]
        b = [3, 4, 5, 6]
        res = []
        set_difference(a, b, res.append)
        self.assertEqual(res, [1, 2])

    def test_set_symmetric_difference(self):
        # elements in A or B but not both
        a = [1, 2, 3]
        b = [3, 4, 5]
        res = []
        set_symmetric_difference(a, b, res.append)
        self.assertEqual(res, [1, 2, 4, 5])

if __name__ == '__main__':
    unittest.main()
