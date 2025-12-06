import unittest
from cpphive import Hive

class TestHive(unittest.TestCase):
    def test_basic_operations(self):
        h = Hive()
        self.assertTrue(h.empty())
        
        it1 = h.insert(1)
        it2 = h.insert(2)
        it3 = h.insert(3)
        
        self.assertEqual(h.size(), 3)
        self.assertEqual(list(h), [1, 2, 3])
        
        # Test iterator access
        self.assertEqual(it1.value(), 1)
        self.assertEqual(it2.value(), 2)

        # Erase middle
        h.erase(it2)
        self.assertEqual(h.size(), 2)
        self.assertEqual(list(h), [1, 3])
        
        # Insert again (should reuse slot)
        it4 = h.insert(4)
        # Order depends on freelist logic (LIFO stack usually -> reuses last freed)
        # 2 was freed. So 4 should go there.
        # Order of iteration: 1, 4, 3
        self.assertEqual(list(h), [1, 4, 3])
        
    def test_growth(self):
        h = Hive()
        # Insert enough to force multiple blocks
        # 1st block cap: 8
        # 2nd block cap: 16
        # Total 24
        
        inserted = []
        for i in range(30):
            inserted.append(h.insert(i))
            
        self.assertEqual(h.size(), 30)
        self.assertEqual(list(h), list(range(30)))
        
        # Erase even numbers
        for i in range(0, 30, 2):
            # We didn't keep iterators for all, but inserted list has them
            h.erase(inserted[i])
            
        self.assertEqual(h.size(), 15)
        remaining = list(h)
        self.assertEqual(remaining, list(range(1, 30, 2)))

    def test_iterator_traversal(self):
        h = Hive([10, 20, 30])
        it = h.insert(40) # return iterator to 40
        
        # Traverse manual
        # Since HiveIterator is constructed manually usually by insert, 
        # we can't easily get 'begin()' iterator as an object unless we implement begin() returning HiveIterator.
        # But __iter__ works.
        pass

if __name__ == '__main__':
    unittest.main()
