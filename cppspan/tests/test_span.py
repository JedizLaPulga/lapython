import unittest
from cppspan import Span
import sys
import os

# Ensure we can import modules from sibling directories for integration tests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../cppvector/src')))
try:
    from cppvector import Vector
except ImportError:
    Vector = None

class TestSpan(unittest.TestCase):
    def test_basic_list(self):
        data = [1, 2, 3, 4, 5]
        s = Span(data)
        self.assertEqual(len(s), 5)
        self.assertFalse(s.empty())
        self.assertEqual(s.size(), 5)
        self.assertEqual(s[0], 1)
        self.assertEqual(s.back(), 5)
        
        # Mutation
        s[0] = 10
        self.assertEqual(data[0], 10) # Should modify underlying list

    def test_subspan(self):
        data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        s = Span(data)
        
        sub = s.subspan(2, 5) # Start at 2, length 5 => [2, 3, 4, 5, 6]
        self.assertEqual(len(sub), 5)
        self.assertEqual(sub[0], 2)
        self.assertEqual(sub.back(), 6)
        
        # Modify subspan
        sub[0] = 99
        self.assertEqual(data[2], 99)
        
        # First / Last
        f = s.first(3) # [0, 1, 99]
        self.assertEqual(len(f), 3)
        self.assertEqual(f[2], 99)
        
        l = s.last(2) # [8, 9]
        self.assertEqual(len(l), 2)
        self.assertEqual(l[0], 8)
        
    def test_recursive_span(self):
        data = [10, 20, 30, 40]
        s1 = Span(data)
        s2 = Span(s1, 1, 2) # [20, 30]
        
        self.assertEqual(len(s2), 2)
        self.assertEqual(s2[0], 20)
        
        # Check internal storage (should be flattened)
        # We can't strictly check private _offset easily without peeking, but behavior verifies it
        s2[1] = 300
        self.assertEqual(data[2], 300)

    def test_from_vector(self):
        if Vector is None:
            print("Skipping Vector test (cppvector not found)")
            return
            
        v = Vector()
        v.push_back(1)
        v.push_back(2)
        v.push_back(3)
        
        s = Span(v)
        self.assertEqual(s.size(), 3)
        self.assertEqual(s[1], 2)
        
        s[1] = 20
        self.assertEqual(v[1], 20)
        
    def test_bounds(self):
        data = [1, 2, 3]
        s = Span(data)
        
        with self.assertRaises(IndexError):
            _ = s[3]
            
        with self.assertRaises(IndexError):
            _ = s.subspan(2, 5) # Too long

    def test_sliced_span(self):
        data = [1, 2, 3, 4]
        s = Span(data)
        s2 = s[1:3] # [2, 3]
        self.assertIsInstance(s2, Span)
        self.assertEqual(len(s2), 2)
        self.assertEqual(s2[0], 2)
        
if __name__ == '__main__':
    unittest.main()
