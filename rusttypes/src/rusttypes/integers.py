from typing import Union, Type, TypeVar

T = TypeVar('T', bound='FixedInt')

class FixedInt:
    _MIN: int = 0
    _MAX: int = 0
    _BITS: int = 0
    _SIGNED: bool = False

    __slots__ = ('_value',)

    def __init__(self, value: Union[int, 'FixedInt']):
        if isinstance(value, FixedInt):
            val = value._value
        else:
            val = int(value)
        
        self._check_bounds(val)
        self._value = val

    @classmethod
    def _check_bounds(cls, value: int):
        if not (cls._MIN <= value <= cls._MAX):
            raise OverflowError(f"Value {value} is out of bounds for {cls.__name__} ({cls._MIN}..={cls._MAX})")

    def __repr__(self):
        return f"{self.__class__.__name__}({self._value})"

    def __str__(self):
        return str(self._value)
    
    def __int__(self):
        return self._value

    def __eq__(self, other):
        if isinstance(other, FixedInt):
            return self._value == other._value
        return self._value == other

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        val = other._value if isinstance(other, FixedInt) else other
        return self._value < val

    def __le__(self, other):
        val = other._value if isinstance(other, FixedInt) else other
        return self._value <= val

    def __gt__(self, other):
        val = other._value if isinstance(other, FixedInt) else other
        return self._value > val

    def __ge__(self, other):
        val = other._value if isinstance(other, FixedInt) else other
        return self._value >= val

    def __hash__(self):
        return hash((self.__class__, self._value))

    # Arithmetic operations
    def __add__(self: T, other) -> T:
        val = other._value if isinstance(other, FixedInt) else other
        return self.__class__(self._value + val)

    def __sub__(self: T, other) -> T:
        val = other._value if isinstance(other, FixedInt) else other
        return self.__class__(self._value - val)

    def __mul__(self: T, other) -> T:
        val = other._value if isinstance(other, FixedInt) else other
        return self.__class__(self._value * val)

    def __floordiv__(self: T, other) -> T:
        val = other._value if isinstance(other, FixedInt) else other
        return self.__class__(self._value // val)
    
    def __truediv__(self: T, other) -> T:
        # Rust integer division is truncated, equivalent to floordiv in Python for positive ops, 
        # but Python floordiv rounds towards negative infinity. Rust rounds towards zero.
        # However, for simplicity and Python compatibility, let's stick to Python semantics OR implement Rust's.
        # User requested "Rust types", so round towards zero is more appropriate?
        # Actually standard / in Python is float. // is int.
        # Rust / on integers is integer division.
        val = other._value if isinstance(other, FixedInt) else other
        return self.__class__(int(self._value / val))

    def __mod__(self: T, other) -> T:
        val = other._value if isinstance(other, FixedInt) else other
        return self.__class__(self._value % val)

    def __pow__(self: T, other) -> T:
        val = other._value if isinstance(other, FixedInt) else other
        return self.__class__(self._value ** val)
    
    def __lshift__(self: T, other) -> T:
        val = other._value if isinstance(other, FixedInt) else other
        return self.__class__(self._value << val)

    def __rshift__(self: T, other) -> T:
        val = other._value if isinstance(other, FixedInt) else other
        return self.__class__(self._value >> val)
    
    def __and__(self: T, other) -> T:
        val = other._value if isinstance(other, FixedInt) else other
        return self.__class__(self._value & val)
    
    def __xor__(self: T, other) -> T:
        val = other._value if isinstance(other, FixedInt) else other
        return self.__class__(self._value ^ val)
    
    def __or__(self: T, other) -> T:
        val = other._value if isinstance(other, FixedInt) else other
        return self.__class__(self._value | val)
        
    def __neg__(self: T) -> T:
        return self.__class__(-self._value)
    
    def __invert__(self: T) -> T:
        # Bitwise NOT in Python is ~x = -x - 1.
        # For fixed width, it depends. usually we mask.
        if self._SIGNED:
            return self.__class__(~self._value)
        else:
            # For unsigned, logical not is usually (MAX ^ val)
            return self.__class__(self._MAX ^ self._value)
            
    def __abs__(self: T) -> T:
        return self.__class__(abs(self._value))

    # Reverse arithmetic
    def __radd__(self: T, other) -> T:
        return self + other
    
    def __rsub__(self: T, other) -> T:
        # other - self 
        val = other._value if isinstance(other, FixedInt) else other
        return self.__class__(val - self._value)
        
    def __rmul__(self: T, other) -> T:
        return self * other
        
    def __rfloordiv__(self: T, other) -> T:
        val = other._value if isinstance(other, FixedInt) else other
        return self.__class__(val // self._value)

    def __rtruediv__(self: T, other) -> T:
        val = other._value if isinstance(other, FixedInt) else other
        return self.__class__(int(val / self._value))
        
    def __rmod__(self: T, other) -> T:
        val = other._value if isinstance(other, FixedInt) else other
        return self.__class__(val % self._value)

class i8(FixedInt):
    _BITS = 8
    _SIGNED = True
    _MIN = -128
    _MAX = 127

class i16(FixedInt):
    _BITS = 16
    _SIGNED = True
    _MIN = -32768
    _MAX = 32767

class i32(FixedInt):
    _BITS = 32
    _SIGNED = True
    _MIN = -2147483648
    _MAX = 2147483647

class i64(FixedInt):
    _BITS = 64
    _SIGNED = True
    _MIN = -9223372036854775808
    _MAX = 9223372036854775807

class u8(FixedInt):
    _BITS = 8
    _SIGNED = False
    _MIN = 0
    _MAX = 255

class u16(FixedInt):
    _BITS = 16
    _SIGNED = False
    _MIN = 0
    _MAX = 65535

class u32(FixedInt):
    _BITS = 32
    _SIGNED = False
    _MIN = 0
    _MAX = 4294967295

class u64(FixedInt):
    _BITS = 64
    _SIGNED = False
    _MIN = 0
    _MAX = 18446744073709551615
