import unittest
from cpparray.array import Array

class TestArray(unittest.TestCase):
    def test_construction(self):
        # Default fill
        a = Array(5, init_value=0)
        self.assertEqual(len(a), 5)
        self.assertEqual(list(a), [0, 0, 0, 0, 0])

        # Source init
        b = Array(3, source=[1, 2, 3])
        self.assertEqual(list(b), [1, 2, 3])

        # Partial init
        c = Array(4, source=[1, 2], init_value=9)
        self.assertEqual(list(c), [1, 2, 9, 9])
        
        # Overflow init
        with self.assertRaises(IndexError):
            Array(2, source=[1, 2, 3])

    def test_access(self):
        a = Array(3, source=[10, 20, 30])
        
        # operator[]
        self.assertEqual(a[0], 10)
        self.assertEqual(a[-1], 30)
        
        # at()
        self.assertEqual(a.at(1), 20)
        with self.assertRaises(IndexError):
            a.at(3)
            
        # front/back
        self.assertEqual(a.front(), 10)
        self.assertEqual(a.back(), 30)

    def test_mutation(self):
        a = Array(2, init_value=0)
        a[0] = 5
        a[1] = 6
        self.assertEqual(list(a), [5, 6])
        
        # Fill
        a.fill(99)
        self.assertEqual(list(a), [99, 99])

    def test_fixed_size(self):
        a = Array(5)
        self.assertEqual(a.size(), 5)
        self.assertEqual(a.max_size(), 5)
        # Python dynamic attributes aside, our API has no resize/push methods
        self.assertFalse(hasattr(a, 'append'))
        self.assertFalse(hasattr(a, 'push_back'))

    def test_swap(self):
        a = Array(3, source=[1, 1, 1])
        b = Array(3, source=[2, 2, 2])
        
        a.swap(b)
        self.assertEqual(list(a), [2, 2, 2])
        self.assertEqual(list(b), [1, 1, 1])
        
        # Swap size mismatch
        c = Array(4)
        with self.assertRaises(ValueError):
            a.swap(c)

if __name__ == '__main__':
    unittest.main()
