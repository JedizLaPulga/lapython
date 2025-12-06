import unittest
from cppunordered_multiset import UnorderedMultiSet

class TestUnorderedMultiSet(unittest.TestCase):
    def test_basic_insertion(self):
        ms = UnorderedMultiSet()
        ms.insert(10)
        ms.insert(10)
        ms.insert(5)
        
        self.assertEqual(ms.size(), 3)
        self.assertEqual(ms.count(10), 2)
        
    def test_erase(self):
        ms = UnorderedMultiSet()
        for _ in range(5):
            ms.insert(100)
        ms.insert(200)
        
        removed = ms.erase(100)
        self.assertEqual(removed, 5)
        self.assertEqual(ms.size(), 1)
        self.assertTrue(ms.contains(200))

    def test_buckets(self):
        ms = UnorderedMultiSet(bucket_count=4)
        for i in range(100):
            ms.insert(i)
        
        self.assertTrue(ms.bucket_count() > 4) # Should have rehashed
        
if __name__ == '__main__':
    unittest.main()
