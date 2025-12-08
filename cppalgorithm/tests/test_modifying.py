import unittest
from cppalgorithm import (
    copy, copy_if, copy_n, fill, fill_n,
    generate, transform, replace, replace_if
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

if __name__ == '__main__':
    unittest.main()
