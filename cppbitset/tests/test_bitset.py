import unittest
from cppbitset.bitset import Bitset

class TestBitset(unittest.TestCase):
    def test_init(self):
        b = Bitset(8, 5) # 00000101
        self.assertEqual(b.to_string(), "00000101")
        self.assertEqual(b.count(), 2)
        
        b2 = Bitset(4, "1111")
        self.assertEqual(b2.to_ulong(), 15)
        self.assertTrue(b2.all())

        # Test truncation initialization
        b3 = Bitset(3, 15) # 1111 -> should become 111 (7)
        self.assertEqual(b3.to_ulong(), 7)

    def test_element_access(self):
        # bitset<4> aka 3 2 1 0
        b = Bitset(4)
        b[0] = True
        b[2] = True
        # Val should be 1010 -> 5 (dec)
        self.assertEqual(b.to_ulong(), 5)
        self.assertTrue(b[0])
        self.assertFalse(b[1])
        self.assertTrue(b.test(2))
        self.assertFalse(b.test(3))
        
        with self.assertRaises(IndexError):
            b[4] = 1

    def test_modifiers(self):
        b = Bitset(5)
        b.set() # all 1
        self.assertEqual(b.count(), 5)
        self.assertTrue(b.all())
        
        b.reset()
        self.assertTrue(b.none())
        
        b.set(1)
        b.flip(1)
        self.assertFalse(b[1])
        
        b.set(1)
        b.flip()
        # 00010 -> 11101
        self.assertTrue(b[0])
        self.assertFalse(b[1])
        self.assertTrue(b[4])

    def test_bitwise_ops(self):
        b1 = Bitset(4, "1010")
        b2 = Bitset(4, "0011")
        
        # AND: 0010
        self.assertEqual((b1 & b2).to_string(), "0010")
        # OR:  1011
        self.assertEqual((b1 | b2).to_string(), "1011")
        # XOR: 1001
        self.assertEqual((b1 ^ b2).to_string(), "1001")
        
        # NOT: 0101
        self.assertEqual((~b1).to_string(), "0101")
        
        # Shift
        b3 = Bitset(4, "0011")
        self.assertEqual((b3 << 1).to_string(), "0110")
        self.assertEqual((b3 >> 1).to_string(), "0001")

if __name__ == '__main__':
    unittest.main()
