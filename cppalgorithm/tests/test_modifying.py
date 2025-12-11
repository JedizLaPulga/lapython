import unittest
from cppalgorithm import (
    copy, copy_if, copy_n, fill, fill_n,
    generate, transform, replace, replace_if,
    remove, remove_if, unique, reverse, rotate,
    shuffle, partition, stable_partition,
    next_permutation, prev_permutation
)

class TestModifying(unittest.TestCase):
    def test_copy_append(self):
        # Test "back_inserter" style
        src = [1, 2, 3]
        dest = []
        copy(src, dest.append)
        self.assertEqual(dest, [1, 2, 3])

    def test_copy_overwrite(self):
        # Test overwriting existing buffer
        src = [10, 20]
        dest = [0, 0, 0, 0]
        copy(src, dest)
        # Should only overwrite first 2
        self.assertEqual(dest, [10, 20, 0, 0])

    def test_copy_if(self):
        src = [1, 2, 3, 4, 5]
        dest = []
        copy_if(src, dest.append, lambda x: x % 2 == 0)
        self.assertEqual(dest, [2, 4])

    def test_fill(self):
        data = [1, 2, 3]
        fill(data, 9)
        self.assertEqual(data, [9, 9, 9])
        
    def test_fill_n(self):
        data = [0, 0, 0, 0]
        fill_n(data, 2, 5)
        self.assertEqual(data, [5, 5, 0, 0])

    def test_transform(self):
        src = [1, 2, 3]
        dest = []
        transform(src, dest.append, lambda x: x * 10)
        self.assertEqual(dest, [10, 20, 30])
        
        # In-place transform (if src is mutable and passed as dest)
        data = [1, 2, 3]
        transform(data, data, lambda x: x + 1)
        self.assertEqual(data, [2, 3, 4])

    def test_replace(self):
        data = [1, 2, 1, 3]
        replace(data, 1, 99)
        self.assertEqual(data, [99, 2, 99, 3])

    def test_replace_if(self):
        data = [1, 2, 3, 4]
        # Replace evens with 0
        replace_if(data, lambda x: x % 2 == 0, 0)
        self.assertEqual(data, [1, 0, 3, 0])

    def test_remove(self):
        data = [1, 2, 3, 1, 4, 1]
        new_end = remove(data, 1)
        self.assertEqual(new_end, 3)
        # Content after new_end is unspecified but typically shifted
        self.assertEqual(data[:new_end], [2, 3, 4])

    def test_remove_if(self):
        data = [1, 2, 3, 4, 5, 6]
        # Remove odds
        new_end = remove_if(data, lambda x: x % 2 != 0)
        self.assertEqual(new_end, 3)
        self.assertEqual(data[:new_end], [2, 4, 6])

    def test_unique(self):
        data = [1, 1, 2, 2, 2, 3, 1, 4, 4]
        new_end = unique(data)
        self.assertEqual(new_end, 5)
        self.assertEqual(data[:new_end], [1, 2, 3, 1, 4])
        
    def test_reverse(self):
        data = [1, 2, 3]
        reverse(data)
        self.assertEqual(data, [3, 2, 1])
        
    def test_rotate(self):
        data = [1, 2, 3, 4, 5]
        # rotate left by 2 (element at index 2 becomes first)
        new_first_idx = rotate(data, 2)
        # Result should be [3, 4, 5, 1, 2]
        self.assertEqual(data, [3, 4, 5, 1, 2]) 
        
    def test_shuffle(self):
        data = [1, 2, 3, 4, 5]
        orig = data[:]
        shuffle(data)
        self.assertEqual(len(data), 5)
        self.assertEqual(set(data), set(orig))
        # Probability of same order is low but non-zero
        
    def test_partition(self):
        data = [1, 2, 3, 4, 5, 6]
        # Partition evens first
        pivot = partition(data, lambda x: x % 2 == 0)
        # Evens should be in data[:pivot], odds in data[pivot:]
        for x in data[:pivot]:
            self.assertTrue(x % 2 == 0)
        for x in data[pivot:]:
            self.assertTrue(x % 2 != 0)
            
    def test_stable_partition(self):
        # Use tuples to verify stability: (value, original_index)
        data = [(2,0), (1,1), (4,2), (3,3), (6,4), (5,5)]
        # Partition evens
        pivot = stable_partition(data, lambda x: x[0] % 2 == 0)
        
        evens = data[:pivot]
        odds = data[pivot:]
        
        self.assertEqual(len(evens), 3)
        self.assertEqual(len(odds), 3)
        
        # Check values
        self.assertTrue(all(x[0] % 2 == 0 for x in evens))
        self.assertTrue(all(x[0] % 2 != 0 for x in odds))
        
        # Check stability (indices should be increasing)
        self.assertEqual([x[1] for x in evens], [0, 2, 4])
        self.assertEqual([x[1] for x in odds], [1, 3, 5])

    def test_next_permutation(self):
        data = [1, 2, 3]
        self.assertTrue(next_permutation(data))
        self.assertEqual(data, [1, 3, 2])
        self.assertTrue(next_permutation(data))
        self.assertEqual(data, [2, 1, 3])
        self.assertTrue(next_permutation(data))
        self.assertEqual(data, [2, 3, 1])
        self.assertTrue(next_permutation(data))
        self.assertEqual(data, [3, 1, 2])
        self.assertTrue(next_permutation(data))
        self.assertEqual(data, [3, 2, 1])
        self.assertFalse(next_permutation(data))
        self.assertEqual(data, [1, 2, 3]) # wrapped around
        
    def test_prev_permutation(self):
        data = [1, 2, 3]
        # Start from [1, 2, 3], prev should be False and wrap to [3, 2, 1]
        self.assertFalse(prev_permutation(data))
        self.assertEqual(data, [3, 2, 1])
        
        self.assertTrue(prev_permutation(data))
        self.assertEqual(data, [3, 1, 2])

if __name__ == '__main__':
    unittest.main()
