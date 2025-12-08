import unittest
from cppflat_set import FlatSet

class TestFlatSet(unittest.TestCase):
    def test_basic_ops(self):
        s = FlatSet()
        self.assertTrue(s.empty())
        
        s.insert(10)
        self.assertEqual(s.size(), 1)
        self.assertTrue(s.contains(10))
        
        # Duplicate insert
        res = s.insert(10)
        self.assertFalse(res)
        self.assertEqual(s.size(), 1)
        
        s.insert(20)
        self.assertEqual(s.size(), 2)

    def test_sorted_construction(self):
        data = [5, 1, 3, 2, 4, 1, 5]
        s = FlatSet(data)
        
        self.assertEqual(s.size(), 5)
        # Should be [1, 2, 3, 4, 5]
        self.assertEqual(list(s), [1, 2, 3, 4, 5])
        
    def test_erase(self):
        s = FlatSet([1, 2, 3])
        self.assertEqual(s.erase(2), 1)
        self.assertEqual(list(s), [1, 3])
        self.assertEqual(s.erase(99), 0)

    def test_bounds(self):
        s = FlatSet([10, 20, 30])
        self.assertEqual(s.lower_bound(15), 1) # index of 20
        self.assertEqual(s.upper_bound(20), 2) # index of 30
        
if __name__ == '__main__':
    unittest.main()
