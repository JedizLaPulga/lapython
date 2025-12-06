import unittest
from cppunordered_multimap import UnorderedMultiMap

class TestUnorderedMultiMap(unittest.TestCase):
    def test_basic_insertion(self):
        mm = UnorderedMultiMap()
        mm.insert(1, 'one')
        mm.insert(1, 'uuno') # Duplicate key
        mm.insert(2, 'two')
        
        self.assertEqual(mm.size(), 3)
        self.assertEqual(mm.count(1), 2)
        self.assertEqual(mm.count(2), 1)
        self.assertEqual(mm.count(99), 0)

    def test_erase(self):
        mm = UnorderedMultiMap()
        mm.insert(1, 'a')
        mm.insert(1, 'b')
        mm.insert(1, 'c')
        mm.insert(2, 'd')
        
        removed = mm.erase(1)
        self.assertEqual(removed, 3)
        self.assertEqual(mm.size(), 1)
        self.assertEqual(mm.count(1), 0)
        
    def test_rehash(self):
        mm = UnorderedMultiMap(bucket_count=2)
        # Should rehash automatically
        for i in range(10):
            mm.insert(i, str(i))
            
        self.assertEqual(mm.size(), 10)
        self.assertTrue(mm.bucket_count() > 2)

    def test_equal_range(self):
        mm = UnorderedMultiMap()
        mm.insert(10, 'x')
        mm.insert(10, 'y')
        
        er = list(mm.equal_range(10))
        self.assertEqual(len(er), 2)
        self.assertTrue((10, 'x') in er)
        self.assertTrue((10, 'y') in er)

if __name__ == '__main__':
    unittest.main()
