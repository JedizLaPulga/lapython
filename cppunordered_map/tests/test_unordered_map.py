import unittest
from cppunordered_map.unordered_map import UnorderedMap

class TestUnorderedMap(unittest.TestCase):
    def test_basic_crud(self):
        m = UnorderedMap()
        m["a"] = 1
        m["b"] = 2
        
        self.assertEqual(m["a"], 1)
        self.assertEqual(m.size(), 2)
        
        m["a"] = 100 # Update
        self.assertEqual(m["a"], 100)
        
        m.erase("a")
        self.assertEqual(m.size(), 1)
        with self.assertRaises(KeyError):
            _ = m["a"]

    def test_buckets(self):
        m = UnorderedMap(bucket_count=2)
        m[1] = "1"
        m[2] = "2" # With only 2 buckets, collision is likely or forced
        m[3] = "3" 
        
        # Check load factor logic
        self.assertTrue(m.load_factor() > 0)
        
        # If automatic rehash happened, count increased
        if m.bucket_count() > 2:
            self.assertTrue(m.bucket_count() >= 4)

    def test_collision_handling(self):
        # Force collision by small bucket count or mock hash? 
        # Standard hash is unpredictable in Python run-to-run, but low bucket count ensures chaining.
        m = UnorderedMap(bucket_count=1) # Everything in bucket 0
        m["x"] = 1
        m["y"] = 2
        
        self.assertEqual(m.bucket_size(0), 2)
        self.assertEqual(m["x"], 1)
        self.assertEqual(m["y"], 2)
        
        m.erase("x")
        self.assertEqual(m.bucket_size(0), 1)
        self.assertEqual(m["y"], 2)

if __name__ == '__main__':
    unittest.main()
