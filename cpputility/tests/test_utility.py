import unittest
from cpputility import (
    Pair, Optional, nullopt, Variant, holds_alternative, get, visit,
    swap, exchange, as_const, cmp_equal, cmp_less, in_range,
    Any, make_any, any_cast, BadAnyCast,
    Expected, Unexpected, BadExpectedAccess,
    Ref, ref, cref
)

class TestPair(unittest.TestCase):
    def test_basic(self):
        p = Pair(1, "s")
        self.assertEqual(p.first, 1)
        self.assertEqual(p.second, "s")
        
        p.first = 2
        self.assertEqual(p.first, 2)
        
    def test_swap(self):
        p1 = Pair(1, 2)
        p2 = Pair(3, 4)
        p1.swap(p2)
        self.assertEqual(p1.first, 3)
        self.assertEqual(p2.first, 1)

    def test_compare(self):
        self.assertTrue(Pair(1, 2) < Pair(1, 3))
        self.assertTrue(Pair(1, 2) < Pair(2, 0))
        self.assertTrue(Pair(1, 5) > Pair(1, 4))
        self.assertEqual(Pair(10, 20), Pair(10, 20))

    def test_iter(self):
        p = Pair(10, 20)
        a, b = p
        self.assertEqual(a, 10)
        self.assertEqual(b, 20)

class TestOptional(unittest.TestCase):
    def test_basic(self):
        o = Optional(42)
        self.assertTrue(o.has_value())
        self.assertTrue(o)
        self.assertEqual(o.value(), 42)
        
    def test_nullopt(self):
        o = Optional(nullopt)
        self.assertFalse(o.has_value())
        self.assertFalse(o)
        with self.assertRaises(RuntimeError):
            o.value()
        self.assertEqual(o.value_or(100), 100)

    def test_reset(self):
        o = Optional(5)
        o.reset()
        self.assertFalse(o.has_value())

    def test_compare(self):
        o1 = Optional(10)
        o2 = Optional(20)
        n = Optional(nullopt)
        
        self.assertTrue(o1 < o2)
        self.assertTrue(n < o1)
        self.assertEqual(o1, Optional(10))
        self.assertNotEqual(o1, n)

class TestVariant(unittest.TestCase):
    def test_basic(self):
        v = Variant(42)
        self.assertTrue(holds_alternative(v, int))
        self.assertFalse(holds_alternative(v, str))
        self.assertEqual(get(v, int), 42)
        
        v = Variant("hello")
        self.assertTrue(holds_alternative(v, str))
        
    def test_visit(self):
        v = Variant(10)
        res = visit(lambda x: x * 2, v)
        self.assertEqual(res, 20)

class TestOps(unittest.TestCase):
    def test_swap(self):
        arr = [1, 2, 3]
        swap(arr, 0, 2)
        self.assertEqual(arr, [3, 2, 1])
        
    def test_exchange(self):
        arr = [10]
        old = exchange(arr, 0, 20)
        self.assertEqual(old, 10)
        self.assertEqual(arr[0], 20)
        
    def test_as_const(self):
        self.assertEqual(as_const(42), 42)
        
    def test_cmp(self):
        self.assertTrue(cmp_equal(10, 10))
        self.assertFalse(cmp_equal(10, 20))
        self.assertTrue(cmp_less(10, 20))
        self.assertFalse(cmp_less(20, 10))
        
    def test_in_range(self):
        self.assertTrue(in_range(5, 1, 10))
        self.assertFalse(in_range(0, 1, 10))
        self.assertFalse(in_range(11, 1, 10))

class TestAny(unittest.TestCase):
    def test_basic(self):
        a = Any(42)
        self.assertTrue(a.has_value())
        self.assertEqual(a.type(), int)
        self.assertEqual(any_cast(a, int), 42)
        
        a = make_any("hello")
        self.assertTrue(a.has_value())
        self.assertEqual(a.type(), str)
        self.assertEqual(any_cast(a, str), "hello")
        
    def test_empty(self):
        a = Any()
        self.assertFalse(a.has_value())
        self.assertEqual(a.type(), type(None))
        with self.assertRaises(BadAnyCast):
            any_cast(a, int)
            
    def test_bad_cast(self):
        a = Any(10)
        with self.assertRaises(BadAnyCast):
            any_cast(a, str)
            
    def test_reset(self):
        a = Any(10)
        a.reset()
        self.assertFalse(a.has_value())

class TestExpected(unittest.TestCase):
    def test_value(self):
        e: Expected[int, str] = Expected(42)
        self.assertTrue(e.has_value())
        self.assertTrue(e)
        self.assertEqual(e.value(), 42)
        self.assertEqual(e.value_or(100), 42)
        with self.assertRaises(BadExpectedAccess):
            e.error()
            
    def test_error(self):
        e: Expected[int, str] = Expected(Unexpected("failed"))
        self.assertFalse(e.has_value())
        self.assertFalse(e)
        self.assertEqual(e.error(), "failed")
        self.assertEqual(e.value_or(100), 100)
        with self.assertRaises(BadExpectedAccess):
            e.value()

    def test_equality(self):
        self.assertEqual(Expected(10), Expected(10))
        self.assertNotEqual(Expected(10), Expected(20))
        self.assertEqual(Expected(Unexpected("err")), Expected(Unexpected("err")))
        self.assertNotEqual(Expected(10), Expected(Unexpected(10)))

class TestReferenceWrapper(unittest.TestCase):
    def test_basic(self):
        val = [1, 2, 3]
        r = ref(val)
        self.assertIs(r.get(), val)
        
        cr = cref(val)
        self.assertIs(cr.get(), val)
        
    def test_call(self):
        def add(a, b):
            return a + b
            
        r = ref(add)
        self.assertEqual(r(2, 3), 5)

if __name__ == '__main__':
    unittest.main()
