import unittest
from cppdeque.deque import Deque

class TestDeque(unittest.TestCase):
    def test_push_back_pop_back(self):
        d = Deque()
        for i in range(100):
            d.push_back(i)
        
        self.assertEqual(d.size(), 100)
        self.assertEqual(d.front(), 0)
        self.assertEqual(d.back(), 99)
        self.assertEqual(d[50], 50) # Random access
        
        for i in reversed(range(100)):
            self.assertEqual(d.pop_back(), i)
            
        self.assertTrue(d.empty())

    def test_push_front_pop_front(self):
        d = Deque()
        # Push 0..99 at front -> 99, 98, ... 0
        for i in range(100):
            d.push_front(i)
            
        self.assertEqual(d.size(), 100)
        self.assertEqual(d.front(), 99)
        self.assertEqual(d.back(), 0)
        self.assertEqual(d[0], 99)
        self.assertEqual(d[99], 0)
        
        # Pop all
        for i in reversed(range(100)):
            val = d.pop_front()
            self.assertEqual(val, i)
            
        self.assertTrue(d.empty())

    def test_mixed_ops(self):
        d = Deque([1, 2, 3])
        d.push_front(0) # 0, 1, 2, 3
        d.push_back(4)  # 0, 1, 2, 3, 4
        
        self.assertEqual(list(d), [0, 1, 2, 3, 4])
        
        self.assertEqual(d.pop_front(), 0)
        self.assertEqual(d.pop_back(), 4)
        self.assertEqual(list(d), [1, 2, 3])

    def test_large_scale(self):
        # Trigger multiple block allocations
        d = Deque()
        N = 1000
        for i in range(N):
            d.push_back(i)
            
        # Verify integrity
        for i in range(N):
            self.assertEqual(d[i], i)
            
        # Push front massive amounts
        for i in range(N):
            d.push_front(-i - 1)
            
        # Now range is -N .. -1, 0 .. N-1
        self.assertEqual(d.size(), 2000)
        self.assertEqual(d.front(), -1000)
        self.assertEqual(d.back(), 999)
        self.assertEqual(d[1000], 0)


if __name__ == '__main__':
    unittest.main()
