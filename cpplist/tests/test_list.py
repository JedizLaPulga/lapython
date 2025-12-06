import unittest
from cpplist.list import List

class TestList(unittest.TestCase):
    def test_init_and_push(self):
        l = List()
        self.assertTrue(l.empty())
        self.assertEqual(l.size(), 0)
        
        l.push_back(1)
        l.push_back(2)
        l.push_front(0)
        
        self.assertEqual(list(l), [0, 1, 2])
        self.assertEqual(l.size(), 3)
        self.assertEqual(l.front(), 0)
        self.assertEqual(l.back(), 2)

    def test_pop(self):
        l = List([1, 2, 3])
        self.assertEqual(l.pop_back(), 3)
        self.assertEqual(l.pop_front(), 1)
        self.assertEqual(list(l), [2])
        self.assertEqual(l.size(), 1)
        
        l.pop_back()
        self.assertTrue(l.empty())

    def test_insert_erase(self):
        l = List([1, 2, 3, 4, 5])
        # Insert in middle
        l.insert(2, 99) # [1, 2, 99, 3, 4, 5]
        self.assertEqual(list(l), [1, 2, 99, 3, 4, 5])
        
        # Erase
        l.erase(2)
        self.assertEqual(list(l), [1, 2, 3, 4, 5])
        
        # Insert edges
        l.insert(0, 0)
        l.insert(6, 6)
        self.assertEqual(list(l), [0, 1, 2, 3, 4, 5, 6])

    def test_swap(self):
        l1 = List([1, 2, 3])
        l2 = List([4, 5])
        l1.swap(l2)
        self.assertEqual(list(l1), [4, 5])
        self.assertEqual(list(l2), [1, 2, 3])

    def test_comparisons(self):
        l1 = List([1, 2, 3])
        l2 = List([1, 2, 3])
        l3 = List([1, 2, 4])
        self.assertEqual(l1, l2)
        self.assertNotEqual(l1, l3)
        self.assertTrue(l1 < l3)

if __name__ == '__main__':
    unittest.main()
