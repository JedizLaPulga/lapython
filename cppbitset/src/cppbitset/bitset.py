from __future__ import annotations
from typing import Union, Iterable

from typing import Union, Iterable
from cppbase import Container

class Bitset(Container):
    __slots__ = ('_val', '_nbits')

    def __init__(self, nbits: int, val: Union[int, str, None] = None):
        """
        Fixed-size sequence of N bits.
        
        Args:
            nbits (int): Number of bits (N).
            val: Initial value. Can be integer or binary string (e.g. "1010").
                 If None, initializes to 0.
        """
        if nbits < 0:
            raise ValueError("nbits must be non-negative")
        
        self._nbits = nbits
        self._val = 0
        
        if isinstance(val, int):
            self._val = val & ((1 << nbits) - 1)
        elif isinstance(val, str):
            # Parse binary string. '110' -> 6 (1*4 + 1*2 + 0)
            # std::bitset constructor from string uses index 0 as left-most char? 
            # In C++: string "1100" -> bitset[3]=1, [2]=1, [1]=0, [0]=0.
            # Python int('1100', 2) does exactly this (12).
            # But we might need to truncate if string is longer than nbits.
            # And handles '0b' prefix if present? Let's stick to simple "0101".
            if val.startswith("0b"):
                val = val[2:]
            self._val = int(val, 2) & ((1 << nbits) - 1)

    # --------------------- Element Access ---------------------
    def __getitem__(self, pos: int) -> bool:
        """Access bit at position pos (0 is LSB)."""
        if pos < 0: pos += self._nbits
        if not (0 <= pos < self._nbits):
            raise IndexError("Bitset index out of range")
        return bool((self._val >> pos) & 1)

    def __setitem__(self, pos: int, value: bool):
        if pos < 0: pos += self._nbits
        if not (0 <= pos < self._nbits):
            raise IndexError("Bitset index out of range")
        if value:
            self._val |= (1 << pos)
        else:
            self._val &= ~(1 << pos)

    def test(self, pos: int) -> bool:
        """Checks if bit at pos is set. Throws IndexError if out of bounds."""
        return self[pos]

    # --------------------- Capacity ---------------------
    def size(self) -> int:
        return self._nbits

    def count(self) -> int:
        """Returns number of bits set to true."""
        return bin(self._val).count('1')

    def any(self) -> bool:
        return self._val != 0

    def none(self) -> bool:
        return self._val == 0

    def all(self) -> bool:
        # Check if val == (1<<N) - 1
        return self._val == ((1 << self._nbits) - 1)

    # --------------------- Modifiers ---------------------
    def set(self, pos: int | None = None, val: bool = True):
        """Sets bit at pos to val. If pos is None, sets all bits."""
        if pos is None:
            if val:
                self._val = (1 << self._nbits) - 1
            else:
                self._val = 0
        else:
            self[pos] = val

    def reset(self, pos: int | None = None):
        """Resets bit at pos (to 0). If pos is None, resets all."""
        self.set(pos, False)

    def flip(self, pos: int | None = None):
        """Flips bit at pos. If pos is None, flips all."""
        if pos is None:
            mask = (1 << self._nbits) - 1
            self._val ^= mask
        else:
            if pos < 0: pos += self._nbits
            if not (0 <= pos < self._nbits):
                raise IndexError("Bitset index out of range")
            self._val ^= (1 << pos)

    # --------------------- Conversions ---------------------
    def to_ulong(self) -> int:
        return self._val

    def to_string(self) -> str:
        """Returns string representation (0s and 1s). pos 0 is on the RIGHT."""
        # Python bin() gives '0b101'. We want '0'*padding + '101'.
        s = bin(self._val)[2:] # strip 0b
        return s.zfill(self._nbits)

    # --------------------- Bitwise Operators ---------------------
    def __and__(self, other: 'Bitset') -> 'Bitset':
        if self._nbits != other._nbits: raise ValueError("Bitset size mismatch")
        return Bitset(self._nbits, self._val & other._val)

    def __or__(self, other: 'Bitset') -> 'Bitset':
        if self._nbits != other._nbits: raise ValueError("Bitset size mismatch")
        return Bitset(self._nbits, self._val | other._val)

    def __xor__(self, other: 'Bitset') -> 'Bitset':
        if self._nbits != other._nbits: raise ValueError("Bitset size mismatch")
        return Bitset(self._nbits, self._val ^ other._val)

    def __invert__(self) -> 'Bitset':
        # ~x
        new_val = (~self._val) & ((1 << self._nbits) - 1)
        return Bitset(self._nbits, new_val)

    def __lshift__(self, pos: int) -> 'Bitset':
        new_val = (self._val << pos) & ((1 << self._nbits) - 1)
        return Bitset(self._nbits, new_val)

    def __rshift__(self, pos: int) -> 'Bitset':
        new_val = (self._val >> pos)
        return Bitset(self._nbits, new_val)
    
    # --------------------- Comparisons ---------------------
    def __eq__(self, other):
        if not isinstance(other, Bitset): return False
        return self._nbits == other._nbits and self._val == other._val

    def __repr__(self):
        return f"bitset<{self._nbits}>({self.to_string()})"
