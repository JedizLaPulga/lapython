import unittest
from cppmultimap import MultiMap

class TestMultiMap(unittest.TestCase):
    def test_basic_insertion(self):
        mm = MultiMap()
        mm.insert(1, 'one')
        mm.insert(1, 'uuno') # Duplicate key
        mm.insert(2, 'two')
        
        self.assertEqual(mm.size(), 3)
        self.assertEqual(mm.count(1), 2)
        self.assertEqual(mm.count(2), 1)
        
        # Verify order
        keys = list(x for x in mm)
        self.assertEqual(keys, [1, 1, 2])

    def test_erase(self):
        mm = MultiMap()
        mm.insert(1, 'a')
        mm.insert(1, 'b')
        mm.insert(1, 'c')
        mm.insert(2, 'd')
        
        self.assertEqual(mm.size(), 4)
        
        removed = mm.erase(1)
        self.assertEqual(removed, 3)
        self.assertEqual(mm.size(), 1)
        self.assertEqual(mm.count(1), 0)
        
        items = list(mm.items())
        self.assertEqual(items, [(2, 'd')])

    def test_equal_range(self):
        mm = MultiMap()
        mm.insert(10, 'x')
        mm.insert(10, 'y')
        mm.insert(5, 'z')
        
        er = list(mm.equal_range(10))
        self.assertEqual(len(er), 2)
        # Order of duplicates isn't strictly guaranteed by C++ standard other than implementation defined, 
        # but our implementation typically preserves some insertion order or tree traversal order.
        # We just check values are there.
        values = sorted([v for k, v in er])
        self.assertEqual(values, ['x', 'y'])

if __name__ == '__main__':
    unittest.main()
