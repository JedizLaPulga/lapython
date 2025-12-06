import unittest
from cppmultiset import MultiSet

class TestMultiSet(unittest.TestCase):
    def test_basic_insertion(self):
        ms = MultiSet()
        ms.insert(10)
        ms.insert(10) # Duplicate
        ms.insert(5)
        
        self.assertEqual(ms.size(), 3)
        self.assertEqual(ms.count(10), 2)
        
        # Verify order
        elements = list(ms)
        self.assertEqual(elements, [5, 10, 10])

    def test_erase(self):
        ms = MultiSet()
        for _ in range(5):
            ms.insert(100)
        ms.insert(200)
        
        self.assertEqual(ms.size(), 6)
        
        removed = ms.erase(100)
        self.assertEqual(removed, 5)
        self.assertEqual(ms.size(), 1)
        self.assertTrue(ms.contains(200))
        self.assertFalse(ms.contains(100))

if __name__ == '__main__':
    unittest.main()
