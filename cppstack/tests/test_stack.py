import unittest
from cppstack.stack import Stack

class MockVector:
    def __init__(self):
        self.items = []
    def push_back(self, x): self.items.append(x)
    def pop_back(self): return self.items.pop()
    def back(self): return self.items[-1]
    def empty(self): return len(self.items) == 0
    def size(self): return len(self.items)
    def __repr__(self): return "MockVector"

class TestStack(unittest.TestCase):
    def test_basic_LIFO(self):
        s = Stack()
        self.assertTrue(s.empty())
        
        s.push(1)
        s.push(2)
        s.push(3)
        
        self.assertEqual(s.size(), 3)
        self.assertEqual(s.top(), 3)
        
        s.pop() # removes 3
        self.assertEqual(s.top(), 2)
        
        s.pop() # removes 2
        self.assertEqual(s.top(), 1)
        
        s.pop() # removes 1
        self.assertTrue(s.empty())
        
        with self.assertRaises(IndexError):
            s.top()
        with self.assertRaises(IndexError):
            s.pop()

    def test_dependency_injection(self):
        v = MockVector()
        s = Stack(v)
        
        s.push(100)
        s.push(200)
        
        self.assertEqual(v.items, [100, 200])
        self.assertEqual(s.top(), 200)

if __name__ == '__main__':
    unittest.main()
