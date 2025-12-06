import unittest
from cpppriority_queue.priority_queue import PriorityQueue

class TestPriorityQueue(unittest.TestCase):
    def test_max_heap_properties(self):
        pq = PriorityQueue()
        # Push mixed
        pq.push(10)
        pq.push(30)
        pq.push(20)
        pq.push(5)
        
        # Expect strict Max Heap order: 30, 20, 10, 5
        self.assertEqual(pq.top(), 30)
        pq.pop() # removes 30
        
        self.assertEqual(pq.top(), 20)
        pq.pop() # removes 20
        
        self.assertEqual(pq.top(), 10)
        pq.pop() # removes 10
        
        self.assertEqual(pq.top(), 5)
        pq.pop() # removes 5
        
        self.assertTrue(pq.empty())

    def test_large_input(self):
        pq = PriorityQueue()
        # Push 0..99
        for i in range(100):
            pq.push(i)
            
        # Should come out as 99..0
        last = 100
        while not pq.empty():
            val = pq.top()
            pq.pop()
            self.assertTrue(val < last)
            self.assertEqual(val, last - 1)
            last = val

    def test_empty_exception(self):
        pq = PriorityQueue()
        with self.assertRaises(IndexError):
            pq.top()
        with self.assertRaises(IndexError):
            pq.pop()

if __name__ == '__main__':
    unittest.main()
