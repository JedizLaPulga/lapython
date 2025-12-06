import unittest
from cppset.set import Set

class TestSet(unittest.TestCase):
    def test_sorted_unique(self):
        s = Set([3, 1, 2, 2, 3])
        # Should be 1, 2, 3
        self.assertEqual(list(s), [1, 2, 3])
        self.assertEqual(s.size(), 3)
        self.assertEqual(s.count(2), 1)

    def test_insert_erase(self):
        s = Set()
        s.insert(10)
        s.insert(5)
        self.assertTrue(s.contains(10))
        self.assertTrue(s.contains(5))
        
        s.erase(5)
        self.assertFalse(s.contains(5))
        self.assertEqual(list(s), [10])
        
        s.erase(10)
        self.assertTrue(s.empty())

    def test_bounds(self):
        s = Set([10, 20, 30, 40])
        
        # lower_bound: first >= k
        self.assertEqual(s.lower_bound(20), 20)
        self.assertEqual(s.lower_bound(25), 30)
        
        # upper_bound: first > k
        self.assertEqual(s.upper_bound(20), 30)
        self.assertEqual(s.upper_bound(25), 30)
        self.assertEqual(s.upper_bound(40), None)

if __name__ == '__main__':
    unittest.main()
