import unittest
from cppalgorithm import (
    for_each, find, find_if, find_if_not,
    count, count_if, all_of, any_of, none_of,
    mismatch, equal, is_permutation, lexicographical_compare
)

class TestNonModifying(unittest.TestCase):
    def test_for_each(self):
        data = [1, 2, 3]
        res = []
        for_each(data, lambda x: res.append(x * 2))
        self.assertEqual(res, [2, 4, 6])

    def test_find(self):
        data = [10, 20, 30, 40]
        self.assertEqual(find(data, 30), 2)
        self.assertEqual(find(data, 99), -1)

    def test_find_if(self):
        data = [1, 3, 4, 5]
        # Find first even number
        idx = find_if(data, lambda x: x % 2 == 0)
        self.assertEqual(idx, 2) # element 4

        idx_not_found = find_if(data, lambda x: x > 10)
        self.assertEqual(idx_not_found, -1)

    def test_find_if_not(self):
        data = [1, 3, 5, 4]
        # Find first NOT odd (even)
        idx = find_if_not(data, lambda x: x % 2 != 0)
        self.assertEqual(idx, 3) # element 4

    def test_count(self):
        data = [1, 2, 3, 2, 1, 2]
        self.assertEqual(count(data, 2), 3)
        self.assertEqual(count(data, 99), 0)

    def test_count_if(self):
        data = [1, 2, 3, 4, 5, 6]
        # Count evens
        c = count_if(data, lambda x: x % 2 == 0)
        self.assertEqual(c, 3)

    def test_all_any_none(self):
        data = [2, 4, 6]
        is_even = lambda x: x % 2 == 0
        is_odd = lambda x: x % 2 != 0
        
        self.assertTrue(all_of(data, is_even))
        self.assertFalse(any_of(data, is_odd))
        self.assertTrue(none_of(data, is_odd))
        
        data_mixed = [2, 3, 4]
        self.assertFalse(all_of(data_mixed, is_even))
        self.assertTrue(any_of(data_mixed, is_odd))

    def test_mismatch(self):
        seq1 = [1, 2, 3, 4]
        seq2 = [1, 2, 5, 4]
        self.assertEqual(mismatch(seq1, seq2), (2, 2))
        
        seq3 = [1, 2, 3]
        self.assertEqual(mismatch(seq1, seq3), (3, 3)) # Mismatch at end of shortest
        
        self.assertEqual(mismatch(seq1, seq1), (4, 4)) # Equal
        
    def test_equal(self):
        seq1 = [1, 2, 3]
        seq2 = [1, 2, 3]
        seq3 = [1, 2, 4]
        seq4 = [1, 2, 3, 4]
        
        self.assertTrue(equal(seq1, seq2))
        self.assertFalse(equal(seq1, seq3))
        self.assertFalse(equal(seq1, seq4))
        
    def test_is_permutation(self):
        seq1 = [1, 2, 3]
        seq2 = [3, 1, 2]
        seq3 = [1, 2, 2]
        
        self.assertTrue(is_permutation(seq1, seq2))
        self.assertFalse(is_permutation(seq1, seq3))
        
    def test_lexicographical_compare(self):
        s1 = [1, 2, 3]
        s2 = [1, 2, 4]
        s3 = [1, 2, 3]
        s4 = [1, 2, 3, 0] # longer but prefix matches, s1 ended first -> s1 < s4
        
        self.assertTrue(lexicographical_compare(s1, s2))
        self.assertFalse(lexicographical_compare(s2, s1))
        self.assertFalse(lexicographical_compare(s1, s3)) # Equal is not strictly less
        
        # s1 is shorter than s4, prefix matches.
        # [1, 2, 3] vs [1, 2, 3, 0]
        # s1 ends, s2 has value -> s1 < s4
        self.assertTrue(lexicographical_compare(s1, s4))
        
        s5 = [1, 2]
        self.assertTrue(lexicographical_compare(s5, s1))

if __name__ == '__main__':
    unittest.main()
