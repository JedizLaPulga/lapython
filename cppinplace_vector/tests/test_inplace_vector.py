import unittest
from cppinplace_vector import InplaceVector

class TestInplaceVector(unittest.TestCase):
    def test_basic(self):
        v = InplaceVector(5)
        self.assertEqual(v.max_size(), 5)
        self.assertEqual(v.size(), 0)
        
        v.push_back(1)
        v.push_back(2)
        
        self.assertEqual(v.size(), 2)
        self.assertEqual(v[0], 1)
        self.assertEqual(v[1], 2)

    def test_overflow(self):
        v = InplaceVector(2)
        v.push_back(1)
        v.push_back(2)
        
        with self.assertRaises(MemoryError):
            v.push_back(3)

    def test_try_push(self):
        v = InplaceVector(1)
        self.assertTrue(v.try_push_back(10))
        self.assertFalse(v.try_push_back(20))
        self.assertEqual(v.size(), 1)
        
    def test_resize(self):
        v = InplaceVector(10)
        v.resize(5, 99)
        self.assertEqual(len(v), 5)
        self.assertEqual(v[4], 99)
        
        with self.assertRaises(MemoryError):
            v.resize(11)

if __name__ == '__main__':
    unittest.main()
