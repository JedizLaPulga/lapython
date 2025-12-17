import unittest
from cppstring import String

class TestString(unittest.TestCase):
    def test_init(self):
        s = String("Hello")
        self.assertEqual(str(s), "Hello")
        self.assertEqual(s.size(), 5)
        
        s2 = String(s)
        self.assertEqual(str(s2), "Hello")
        
        s3 = String()
        self.assertTrue(s3.empty())

    def test_sso(self):
        # Default SSO cap is 15
        s = String("123456789012345") # 15 chars
        self.assertEqual(s.size(), 15)
        # Should be small
        self.assertTrue(s._is_small)
        
        s.push_back('6')
        self.assertEqual(s.size(), 16)
        # Should now be large
        self.assertFalse(s._is_small)
        self.assertTrue(s.capacity() >= 16)

    def test_modifiers(self):
        s = String("Hello")
        s.push_back('!')
        self.assertEqual(str(s), "Hello!")
        
        s.pop_back()
        self.assertEqual(str(s), "Hello")
        
        s.append(", World")
        self.assertEqual(str(s), "Hello, World")
        
        s.insert(5, " there")
        self.assertEqual(str(s), "Hello there, World")
        
        s.erase(5, 6) # remove " there" (length 6)
        self.assertEqual(str(s), "Hello, World")
        
        s.replace(7, 5, "Python")
        self.assertEqual(str(s), "Hello, Python")
        
        s.clear()
        self.assertTrue(s.empty())
        self.assertEqual(s.size(), 0)

    def test_access(self):
        s = String("ABC")
        self.assertEqual(s[0], 'A')
        self.assertEqual(s[1], 'B')
        self.assertEqual(s[2], 'C')
        self.assertEqual(s.front(), 'A')
        self.assertEqual(s.back(), 'C')
        
        s[1] = 'Z'
        self.assertEqual(str(s), "AZC")
        
        with self.assertRaises(IndexError):
            _ = s[10]

    def test_iter(self):
        s = String("Hi")
        chars = [c for c in s]
        self.assertEqual(chars, ['H', 'i'])
        
    def test_slice(self):
        s = String("012345")
        sub = s[1:4] # "123"
        self.assertIsInstance(sub, String)
        self.assertEqual(str(sub), "123")
        
    def test_find(self):
        s = String("banana")
        self.assertEqual(s.find("nan"), 2)
        self.assertEqual(s.find("z"), -1)
        self.assertEqual(s.substr(2, 3).c_str(), "nan")

    def test_operators(self):
        s = String("A")
        s += "B"
        self.assertEqual(str(s), "AB")
        
        s2 = s + "C"
        self.assertEqual(str(s2), "ABC")
        self.assertEqual(str(s), "AB") # Original unchanged

    def test_errors(self):
        s = String("A")
        with self.assertRaises(ValueError):
            s.push_back("too long")
        with self.assertRaises(ValueError):
            s[0] = "xx"

if __name__ == '__main__':
    unittest.main()
