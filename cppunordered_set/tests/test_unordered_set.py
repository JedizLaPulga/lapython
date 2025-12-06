import unittest
from cppunordered_set.unordered_set import UnorderedSet

class TestUnorderedSet(unittest.TestCase):
    def test_unique_insert(self):
        s = UnorderedSet()
        s.insert(1)
        s.insert(1) # Duplicate
        s.insert(2)
        
        self.assertEqual(s.size(), 2)
        self.assertTrue(s.contains(1))
        self.assertTrue(s.contains(2))

    def test_erase(self):
        s = UnorderedSet([10, 20, 30])
        self.assertTrue(s.contains(20))
        s.erase(20)
        self.assertFalse(s.contains(20))
        self.assertEqual(s.size(), 2)
        
        s.erase(99) # Not exists
        self.assertEqual(s.size(), 2)

    def test_buckets_growth(self):
        # Start small
        s = UnorderedSet(bucket_count=2)
        for i in range(10):
            s.insert(i)
            
        # Should have rehashed
        self.assertTrue(s.bucket_count() > 2)
        self.assertEqual(s.size(), 10)
        # Verify all elements present
        for i in range(10):
            self.assertTrue(s.contains(i))

if __name__ == '__main__':
    unittest.main()
