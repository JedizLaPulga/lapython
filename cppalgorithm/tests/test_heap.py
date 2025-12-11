import unittest
import cppalgorithm as cpp
import random

class TestHeap(unittest.TestCase):
    def test_make_heap_and_is_heap(self):
        data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
        cpp.make_heap(data)
        self.assertTrue(cpp.is_heap(data))
        # Max element should be at index 0
        self.assertEqual(data[0], 9)
        
        # Test empty
        empty = []
        cpp.make_heap(empty)
        self.assertTrue(cpp.is_heap(empty))
        
        # Test single
        single = [1]
        cpp.make_heap(single)
        self.assertTrue(cpp.is_heap(single))

    def test_push_heap(self):
        data = [9, 5, 4, 1, 1, 3, 2] # Already a heap
        self.assertTrue(cpp.is_heap(data))
        
        # Append new element '6'
        data.append(6)
        # Sift up
        cpp.push_heap(data)
        
        self.assertTrue(cpp.is_heap(data))
        self.assertEqual(data[0], 9) # 9 is still max
        
        # Append new max '10'
        data.append(10)
        cpp.push_heap(data)
        self.assertTrue(cpp.is_heap(data))
        self.assertEqual(data[0], 10)

    def test_pop_heap(self):
        data = [10, 6, 5]
        # Heap: 10
        #      /  \
        #     6    5
        cpp.make_heap(data)
        self.assertTrue(cpp.is_heap(data))
        
        # Pop max (10)
        cpp.pop_heap(data)
        # Now 10 is at end, [0:-1] is heap
        self.assertEqual(data[-1], 10)
        heap_part = data[:-1]
        self.assertTrue(cpp.is_heap(heap_part))
        # New max should be 6
        self.assertEqual(heap_part[0], 6)
        self.assertEqual(len(data), 3) # Length shouldn't change
        
        # Remove it for real
        val = data.pop()
        self.assertEqual(val, 10)
        self.assertTrue(cpp.is_heap(data))

    def test_sort_heap(self):
        data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
        cpp.make_heap(data)
        self.assertTrue(cpp.is_heap(data))
        
        cpp.sort_heap(data)
        # Should be sorted ascending
        self.assertEqual(data, sorted([3, 1, 4, 1, 5, 9, 2, 6, 5, 3]))
        
        # Verify it destroyed the heap property (Max is at end) inside list, essentially sorted
        self.assertTrue(all(data[i] <= data[i+1] for i in range(len(data)-1)))

    def test_is_heap_until(self):
        data = [10, 9, 8, 7, 6, 5, 4]
        self.assertEqual(cpp.is_heap_until(data), len(data))
        
        # Create violation
        # data[1] (9) < data[3] (make it 20) -> violation at index 3?
        # No, parent of 3 is 1 (idx 1). data[1]=9. data[3]=7.
        # If we set data[3] = 20. Call is_heap_until.
        # compare(9, 20) -> 9 < 20 -> True => Violation.
        data_bad = [10, 9, 8, 20, 6, 5, 4]
        # data[0]=10. Children 1, 2 (9, 8). OK.
        # data[1]=9. Children 3, 4 (20, 6). 9 < 20 VIOLATION at index 3.
        self.assertEqual(cpp.is_heap_until(data_bad), 3)

    def test_custom_comparator(self):
        # Min heap using custom comparator (inverted logic)
        # comp(a, b): return a > b
        # Max heap def: parent !< child (using default <)
        # Here: parent !> child implies parent <= child. So Min Heap.
        
        comp = lambda a, b: a > b
        
        data = [3, 1, 4, 1, 5, 9]
        cpp.make_heap(data, comparator=comp)
        
        # Root should be minimum (1)
        self.assertEqual(data[0], 1)
        
        # Check property manually: parent <= child
        for i in range(1, len(data)):
            p = (i - 1) // 2
            # With comp(a,b) = a>b.
            # Heap property: not comp(parent, child)
            # => not (parent > child) => parent <= child.
            self.assertTrue(data[p] <= data[i])
            
        # Push 0
        data.append(0)
        cpp.push_heap(data, comparator=comp)
        self.assertEqual(data[0], 0)
        
        # Sort heap => Descending
        cpp.sort_heap(data, comparator=comp)
        self.assertEqual(data, [9, 5, 4, 3, 1, 1, 0])

    def test_random_fuzz(self):
        for _ in range(10):
            data = [random.randint(0, 100) for _ in range(50)]
            cpp.make_heap(data)
            self.assertTrue(cpp.is_heap(data))
            
            # Push
            new_val = random.randint(0, 100)
            data.append(new_val)
            cpp.push_heap(data)
            self.assertTrue(cpp.is_heap(data))
            
            # Pop
            cpp.pop_heap(data)
            max_val = data.pop()
            self.assertTrue(cpp.is_heap(data))
            
            # Use Python's max to verify
            if data:
                self.assertEqual(max(data), data[0])

if __name__ == '__main__':
    unittest.main()
