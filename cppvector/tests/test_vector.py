import unittest
from cppvector.vector import Vector

class TestVector(unittest.TestCase):
    def test_svo_and_growth(self):
        v = Vector()
        # SVO limits usually 8
        for i in range(10):
            v.push_back(i)
        
        self.assertEqual(len(v), 10)
        self.assertEqual(v[9], 9)
        self.assertEqual(v[0], 0)
    
    def test_access_update(self):
        v = Vector([1, 2, 3])
        self.assertEqual(v[0], 1)
        v[0] = 100
        self.assertEqual(v[0], 100)
        
    def test_sequence_interface(self):
        # Verify it works with cppbase Sequence (implied by inheritance)
        from cppbase import Sequence
        v = Vector()
        self.assertTrue(isinstance(v, Sequence))
        self.assertTrue(isinstance(v, Vector))

if __name__ == '__main__':
    unittest.main()