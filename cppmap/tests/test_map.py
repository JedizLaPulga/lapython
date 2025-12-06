import unittest
from cppmap.map import Map

class TestMap(unittest.TestCase):
    def test_sorted_order(self):
        m = Map()
        m[3] = "three"
        m[1] = "one"
        m[2] = "two"
        
        # Keys should iterate 1, 2, 3
        self.assertEqual(list(m), [1, 2, 3])
        self.assertEqual(list(m.items()), [(1, "one"), (2, "two"), (3, "three")])

    def test_access_update(self):
        m = Map()
        m["a"] = 1
        self.assertEqual(m["a"], 1)
        m["a"] = 2
        self.assertEqual(m["a"], 2)
        
        with self.assertRaises(KeyError):
            val = m["b"]

    def test_erase(self):
        m = Map({1: 1, 2: 2, 3: 3})
        m.erase(2) # Remove middle
        self.assertEqual(list(m), [1, 3])
        
        m.erase(1) # Remove leaf/root?
        self.assertEqual(list(m), [3])
        
        m.erase(3)
        self.assertTrue(m.empty())

    def test_bound_ops(self):
        # 10, 20, 30, 40
        m = Map({10: 'a', 20: 'b', 30: 'c', 40: 'd'})
        
        # lower_bound: first >= k
        self.assertEqual(m.lower_bound(20), 20)
        self.assertEqual(m.lower_bound(25), 30)
        self.assertEqual(m.lower_bound(41), None)
        
        # upper_bound: first > k
        self.assertEqual(m.upper_bound(20), 30)
        self.assertEqual(m.upper_bound(30), 40)
        self.assertEqual(m.upper_bound(40), None)

if __name__ == '__main__':
    unittest.main()
