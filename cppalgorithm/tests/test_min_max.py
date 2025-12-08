import unittest
from cppalgorithm import (
    min_element, max_element,
    minmax_element, clamp
)

class TestMinMax(unittest.TestCase):
    def test_min_element(self):
        data = [5, 1, 9, 2]
        idx = min_element(data)
        self.assertEqual(idx, 1) # Value 1 at index 1
        self.assertEqual(data[idx], 1)
        
    def test_max_element(self):
        data = [5, 1, 9, 2]
        idx = max_element(data)
        self.assertEqual(idx, 2) # Value 9 at index 2
        
    def test_minmax_element(self):
        data = [10, 2, 50, 5]
        mi, ma = minmax_element(data)
        self.assertEqual(mi, 1) # val 2
        self.assertEqual(ma, 2) # val 50
        
    def test_clamp(self):
        self.assertEqual(clamp(5, 0, 10), 5)
        self.assertEqual(clamp(-5, 0, 10), 0)
        self.assertEqual(clamp(15, 0, 10), 10)

if __name__ == '__main__':
    unittest.main()
