import unittest
from rusttypes import i8, i16, i32, i64, u8, u16, u32, u64

class TestRustTypes(unittest.TestCase):
    def test_initialization(self):
        self.assertEqual(int(i8(127)), 127)
        self.assertEqual(int(i8(-128)), -128)
        self.assertEqual(int(u8(255)), 255)
        self.assertEqual(int(u8(0)), 0)
        
        # Test overflow during init
        with self.assertRaises(OverflowError):
            i8(128)
        with self.assertRaises(OverflowError):
            i8(-129)
        with self.assertRaises(OverflowError):
            u8(256)
        with self.assertRaises(OverflowError):
            u8(-1)

    def test_arithmetic(self):
        a = i8(10)
        b = i8(20)
        c = a + b
        self.assertIsInstance(c, i8)
        self.assertEqual(c, 30)
        
        # Test overflow
        a = i8(120)
        b = i8(10)
        with self.assertRaises(OverflowError):
            c = a + b # 130 > 127
            
        # Test underflow
        a = i8(-120)
        b = i8(10)
        with self.assertRaises(OverflowError):
            c = a - b # -130 < -128
            
    def test_unsigned_arithmetic(self):
        a = u8(200)
        b = u8(55)
        c = a + b
        self.assertEqual(c, 255)
        
        with self.assertRaises(OverflowError):
            c = a + u8(56)
            
        # Negative result for unsigned
        a = u8(10)
        b = u8(20)
        with self.assertRaises(OverflowError):
            c = a - b # -10

    def test_mixed_arithmetic(self):
        # Operations with raw python ints should work but return FixedInt
        a = i32(100)
        b = 200
        c = a + b
        self.assertIsInstance(c, i32)
        self.assertEqual(c, 300)
        
        # Reverse op
        c = 200 + a
        self.assertIsInstance(c, i32)
        self.assertEqual(c, 300)

    def test_bitwise(self):
        a = u8(0b10101010)
        b = u8(0b00001111)
        self.assertEqual(a & b, 0b00001010)
        self.assertEqual(a | b, 0b10101111)
        self.assertEqual(a ^ b, 0b10100101)
        
        # Shift
        self.assertEqual(u8(1) << 2, 4)
        self.assertEqual(u8(4) >> 1, 2)
        
        # Inverse
        # For u8: ~00000000 = 11111111 = 255
        self.assertEqual(~u8(0), 255)
        # For i8: ~0 = -1
        self.assertEqual(~i8(0), -1)

    def test_division(self):
        # Rust integer division truncates towards zero
        # Python int(a/b) truncates towards zero. Python a//b truncates towards -inf.
        # My implementation uses int(a/b) for truediv (/) and a//b for floordiv (//).
        
        # 5 / 2 = 2
        self.assertEqual(i8(5) / i8(2), 2)
        # -5 / 2 = -2 (Rust style/int cast)
        self.assertEqual(i8(-5) / i8(2), -2)
        
        # using floor div //
        # -5 // 2 = -3 (Python style)
        self.assertEqual(i8(-5) // i8(2), -3)

    def test_comparisons(self):
        self.assertTrue(i8(10) < i8(20))
        self.assertTrue(i8(20) > 10)
        self.assertTrue(i8(10) == 10)
        self.assertTrue(i8(10) != 11)

    def test_all_types(self):
        types = [i8, i16, i32, i64, u8, u16, u32, u64]
        for t in types:
            # Min
            min_val = t(t._MIN)
            # Max
            max_val = t(t._MAX)
            
            # Check bounds
            with self.assertRaises(OverflowError):
                t(t._MIN - 1)
            with self.assertRaises(OverflowError):
                t(t._MAX + 1)

if __name__ == '__main__':
    unittest.main()
