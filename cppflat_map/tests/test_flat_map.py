import unittest
from cppflat_map import FlatMap

class TestFlatMap(unittest.TestCase):
    def test_basic_ops(self):
        m = FlatMap()
        self.assertTrue(m.empty())
        self.assertEqual(m.size(), 0)
        
        m.insert(1, "one")
        self.assertEqual(m.size(), 1)
        self.assertEqual(m[1], "one")
        
        m[2] = "two"
        self.assertEqual(m.size(), 2)
        self.assertEqual(m[2], "two")
        
        # Overwrite
        m[1] = "ONE"
        self.assertEqual(m[1], "ONE")
        self.assertEqual(m.size(), 2)

    def test_sorted_order(self):
        m = FlatMap()
        # Insert randomized
        m[5] = "e"
        m[1] = "a"
        m[3] = "c"
        m[2] = "b"
        m[4] = "d"
        
        self.assertEqual(m.size(), 5)
        
        # Iteration should be sorted
        keys = list(m)
        self.assertEqual(keys, [1, 2, 3, 4, 5])
        
        values = list(m.values())
        self.assertEqual(values, ["a", "b", "c", "d", "e"])

    def test_erase(self):
        m = FlatMap({1: "a", 2: "b", 3: "c"})
        self.assertEqual(m.erase(2), 1)
        self.assertEqual(list(m), [1, 3])
        self.assertEqual(m.erase(99), 0)

    def test_bounds(self):
        m = FlatMap({10: "x", 20: "y", 30: "z"})
        
        # lower_bound(15) -> index of 20 -> 1
        self.assertEqual(m.lower_bound(15), 1)
        # lower_bound(10) -> index of 10 -> 0
        self.assertEqual(m.lower_bound(10), 0)
        
        # upper_bound(20) -> index of 30 -> 2
        self.assertEqual(m.upper_bound(20), 2)
        
    def test_constructor(self):
        data = [(3, 'c'), (1, 'a'), (2, 'b'), (1, 'duplicate')]
        # Should be sorted, and duplicates typically kept or first found used if we don't purify.
        # Our impl: "if self._keys and self._keys[-1] == k: continue" => First strict wins on sorted.
        # sorted is stable.
        # (1, 'a') comes before (1, 'duplicate'). So 'a' should be kept.
        
        m = FlatMap(data)
        self.assertEqual(list(m), [1, 2, 3])
        self.assertEqual(m[1], 'a')
        self.assertEqual(m[2], 'b')
        self.assertEqual(m[3], 'c')

    def test_insert_or_assign(self):
        m = FlatMap()
        is_new = m.insert_or_assign(1, "one")
        self.assertTrue(is_new)
        self.assertEqual(m[1], "one")
        
        is_new = m.insert_or_assign(1, "ONE")
        self.assertFalse(is_new)
        self.assertEqual(m[1], "ONE")

if __name__ == '__main__':
    unittest.main()
