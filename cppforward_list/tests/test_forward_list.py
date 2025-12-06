import unittest
from cppforward_list.forward_list import ForwardList

class TestForwardList(unittest.TestCase):
    def test_basic_push_pop(self):
        fl = ForwardList()
        fl.push_front(10)
        fl.push_front(20) # 20 -> 10
        
        self.assertEqual(fl.front(), 20)
        self.assertEqual(fl.pop_front(), 20)
        self.assertEqual(fl.front(), 10)
        self.assertEqual(fl.pop_front(), 10)
        self.assertTrue(fl.empty())

    def test_init_iterable(self):
        # Should preserve order
        fl = ForwardList([1, 2, 3])
        self.assertEqual(list(fl), [1, 2, 3])
        self.assertEqual(fl.front(), 1)

    def test_insert_after(self):
        fl = ForwardList([1, 3]) # 1 -> 3
        
        it = fl.begin() # points to 1
        fl.insert_after(it, 2) # 1 -> 2 -> 3
        
        self.assertEqual(list(fl), [1, 2, 3])
        
        # Advance iter
        it.next() # points to 2
        fl.insert_after(it, 99) # 1 -> 2 -> 99 -> 3
        self.assertEqual(list(fl), [1, 2, 99, 3])

    def test_erase_after(self):
        fl = ForwardList([1, 2, 3, 4])
        it = fl.begin() # 1
        
        fl.erase_after(it) # Erase element after 1 (which is 2). List: 1 -> 3 -> 4
        
        self.assertEqual(list(fl), [1, 3, 4])

    def test_reverse(self):
        fl = ForwardList([1, 2, 3])
        fl.reverse()
        self.assertEqual(list(fl), [3, 2, 1])

if __name__ == '__main__':
    unittest.main()
