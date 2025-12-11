import unittest
import cppalgorithm as cpp

class TestAdvancedSearch(unittest.TestCase):
    def test_search(self):
        # search(sequence, subsequence)
        data = [1, 2, 3, 4, 5, 1, 2, 8]
        sub = [1, 2]
        
        # Should find first occurrence at index 0
        self.assertEqual(cpp.search(data, sub), 0)
        
        sub2 = [1, 2, 8]
        # Should find at index 5
        self.assertEqual(cpp.search(data, sub2), 5)
        
        sub3 = [9, 9]
        # Not found
        self.assertEqual(cpp.search(data, sub3), -1)
        
        # Empty sub -> 0
        self.assertEqual(cpp.search(data, []), 0)
        
        # Sub match at end
        self.assertEqual(cpp.search([1, 2, 3], [3]), 2)

    def test_find_end(self):
        # find_end(sequence, subsequence) -> Last occurrence
        data = [1, 2, 3, 1, 2, 3, 4]
        sub = [1, 2]
        
        # First occurrence is 0, second is 3. Should return 3.
        self.assertEqual(cpp.find_end(data, sub), 3)
        
        sub2 = [4]
        self.assertEqual(cpp.find_end(data, sub2), 6)
        
        # Not found
        self.assertEqual(cpp.find_end(data, [9]), -1)

    def test_find_first_of(self):
        # find_first_of(sequence, search_elements)
        data = [10, 20, 30, 40, 50]
        # Find first element in data that is also in [15, 40, 60]
        # 10 no, 20 no, 30 no, 40 YES. Index 3.
        self.assertEqual(cpp.find_first_of(data, [15, 40, 60]), 3)
        
        # Predicate case: find first element divisible by 7 (using search_elements=[7] and mod predicate)
        # That's not how find_first_of works typically with predicate.
        # std::find_first_of(first1, last1, first2, last2, p)
        # returns first iterator i in [first1, last1) such that for some j in [first2, last2), p(*i, *j) is true.
        
        # Find first element in data that is > element in [35]
        # 10>35 F, 20>35 F, 30>35 F, 40>35 T. Index 3.
        self.assertEqual(cpp.find_first_of(data, [35], lambda x, y: x > y), 3)

    def test_adjacent_find(self):
        data = [1, 2, 3, 4, 4, 5]
        # Found 4, 4 at index 3
        self.assertEqual(cpp.adjacent_find(data), 3)
        
        data2 = [1, 2, 3]
        self.assertEqual(cpp.adjacent_find(data2), -1)
        
        # With predicate: find consecutive that sum to 10
        data3 = [1, 2, 5, 5, 8, 2]
        # 1+2=3, 2+5=7, 5+5=10 -> index 2 (element 5)
        self.assertEqual(cpp.adjacent_find(data3, lambda a, b: a + b == 10), 2)

    def test_search_n(self):
        # search_n(sequence, count, value)
        data = [1, 2, 2, 2, 3, 4, 2, 2]
        
        # Find 3 consecutive 2s
        self.assertEqual(cpp.search_n(data, 3, 2), 1)
        
        # Find 4 consecutive 2s -> -1
        self.assertEqual(cpp.search_n(data, 4, 2), -1)
        
        # Find 2 consecutive 2s matches mismatch? No, first sequence of 2.
        # It finds the first occurrence.
        self.assertEqual(cpp.search_n(data, 2, 2), 1)
        
        # Predicate: consecutive elements > 3. Count=2.
        # [1, 2, 2, 2, 3, 4, 2, 2]
        # 3 is not > 3. 4 > 3 (1). 2 nope.
        # Let's try data = [1, 4, 5, 1]
        data_g = [1, 4, 5, 1]
        # search for 2 elements > 3. Value argument is ignored BUT standard search_n is (count, value, predicate).
        # std::search_n(first, last, count, value, pred)
        # Returns first i such that pred(*(i+n), value) is true for all n in [0, count).
        # So we search for sequence where element > 3? No, element matches value with predicate.
        
        # Search for 2 elements greater than 0. (value=0, pred= >)
        # 1>0, 4>0. yes at index 0.
        self.assertEqual(cpp.search_n(data_g, 2, 0, lambda item, val: item > val), 0)

if __name__ == '__main__':
    unittest.main()
