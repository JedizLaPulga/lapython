import unittest
import sys
import os

# We want to test adapting our own cpplist/cppdeque if possible, or just mock it.
# For isolation, I will use the internal default and a Mock.

from cppqueue.queue import Queue

class MockDeque:
    def __init__(self):
        self.items = []
    def push_back(self, x): self.items.append(x)
    def pop_front(self): return self.items.pop(0) # Inefficient but fine for mock
    def front(self): return self.items[0]
    def back(self): return self.items[-1]
    def empty(self): return len(self.items) == 0
    def size(self): return len(self.items)
    def __repr__(self): return "MockDeque"

class TestQueue(unittest.TestCase):
    def test_default_container(self):
        q = Queue()
        self.assertTrue(q.empty())
        
        q.push(10)
        q.push(20)
        
        self.assertEqual(q.size(), 2)
        self.assertEqual(q.front(), 10)
        self.assertEqual(q.back(), 20)
        
        q.pop() # Remove 10
        self.assertEqual(q.front(), 20)
        self.assertEqual(q.size(), 1)
        
        q.pop()
        self.assertTrue(q.empty())

    def test_custom_container(self):
        # Inject our mock deque
        mock = MockDeque()
        q = Queue(mock)
        
        q.push('a')
        q.push('b')
        self.assertEqual(mock.items, ['a', 'b'])
        
        val = q.front()
        self.assertEqual(val, 'a')
        
        q.pop()
        self.assertEqual(mock.items, ['b'])

if __name__ == '__main__':
    unittest.main()
