# vector.py
from __future__ import annotations
from typing import TypeVar, Generic, Iterable, Any, Iterator
import ctypes
import array
import struct

T = TypeVar('T')


from cppbase import Sequence

# =================================================================
# 1. Ultimate Generic Vector<T> with SVO, swap, comparisons, etc.
# =================================================================
class Vector(Sequence, Generic[T]):
    _SVO_CAP = 8
    __slots__ = ('_size', '_is_small', '_small', '_large', '_capacity')

    def __init__(self, source: Iterable[T] | None = None):
        self._size = 0
        self._is_small = True
        self._small = [None] * self._SVO_CAP
        self._large = None
        self._capacity = 0
        if source is not None:
            self.assign(source)

    # --------------------- Internal ---------------------
    def _move_to_large(self, new_cap: int):
        if not self._is_small:
            return
        new_cap = max(new_cap, 16)
        large = (ctypes.py_object * new_cap)()
        for i in range(self._size):
            large[i] = self._small[i]
        self._large = large
        self._capacity = new_cap
        self._is_small = False
        self._small = None

    def _resize(self, new_cap: int):
        if self._is_small and new_cap <= self._SVO_CAP:
            return
        if self._is_small:
            self._move_to_large(new_cap)
            return
        if new_cap == self._capacity:
            return
        new_data = (ctypes.py_object * new_cap)()
        for i in range(self._size):
            new_data[i] = self._large[i]
        self._large = new_data
        self._capacity = new_cap

    # --------------------- Capacity ---------------------
    def size(self) -> int: return self._size
    def capacity(self) -> int: return self._SVO_CAP if self._is_small else self._capacity
    def empty(self) -> bool: return self._size == 0

    def reserve(self, n: int):
        if n > self.capacity():
            self._resize(max(n, self.capacity() * 2 if self.capacity() > 0 else 16))

    def shrink_to_fit(self):
        if self._is_small:
            return
        if self._size <= self._SVO_CAP:
            small = [None] * self._SVO_CAP
            for i in range(self._size):
                small[i] = self._large[i]
            self._small = small
            self._large = None
            self._is_small = True
            self._capacity = 0
        elif self._size < self._capacity:
            self._resize(self._size)

    # --------------------- Modifiers ---------------------
    def assign(self, source: Iterable[T] | int, value: T | None = None):
        self.clear()
        if isinstance(source, int):
            self.resize(source, value)
        else:
            for x in source:
                self.push_back(x)

    def resize(self, new_size: int, value: T | None = None):
        if new_size > self._size:
            self.reserve(new_size)
            for i in range(self._size, new_size):
                self.push_back(value if value is not None else None)
        else:
            self._size = new_size

    def push_back(self, value: T):
        if self._size == self.capacity():
            self.reserve(self._size + 1)
        if self._is_small:
            self._small[self._size] = value
        else:
            self._large[self._size] = value
        self._size += 1

    def pop_back(self) -> T:
        if not self._size:
            raise IndexError("pop_back from empty vector")
        self._size -= 1
        val = (self._small if self._is_small else self._large)[self._size]
        (self._small if self._is_small else self._large)[self._size] = None
        return val

    def clear(self):
        self._size = 0

    def swap(self, other: 'Vector'):
        if self is other:
            return
        (self._size, other._size), \
        (self._is_small, other._is_small), \
        (self._small, other._small), \
        (self._large, other._large), \
        (self._capacity, other._capacity) = \
        (other._size, self._size), \
        (other._is_small, self._is_small), \
        (other._small, self._small), \
        (other._large, self._large), \
        (other._capacity, self._capacity)

    # --------------------- Access ---------------------
    def __getitem__(self, i):
        if i < 0: i += self._size
        if not (0 <= i < self._size):
            raise IndexError("vector index out of range")
        return (self._small if self._is_small else self._large)[i]

    def __setitem__(self, i, v):
        if i < 0: i += self._size
        if not (0 <= i < self._size):
            raise IndexError("vector assignment out of range")
        (self._small if self._is_small else self._large)[i] = v

    def front(self): return self[0]
    def back(self):  return self[self._size - 1]

    # --------------------- Comparisons ---------------------
    def __eq__(self, other): return list(self) == list(other)
    def __ne__(self, other): return not (self == other)
    def __lt__(self, other): return list(self) < list(other)
    def __le__(self, other): return list(self) <= list(other)
    def __gt__(self, other): return list(self) > list(other)
    def __ge__(self, other): return list(self) >= list(other)

    # --------------------- Iterator ---------------------
    def __iter__(self) -> Iterator[T]:
        if self._is_small:
            for i in range(self._size):
                yield self._small[i]
        else:
            for i in range(self._size):
                yield self._large[i]

    def __len__(self): return self._size
    def __repr__(self):
        data = ', '.join(repr(x) for x in self)
        mode = "SVO" if self._is_small else "Heap"
        return f"Vector[{self._size}/{self.capacity()}]({data}) <{mode}>"


# =================================================================
# 2. vector<bool> — bit-packed specialization
# =================================================================
class VectorBool:
    __slots__ = ('_data', '_size')

    def __init__(self, source=None):
        self._data = bytearray()
        self._size = 0
        if source is not None:
            for b in source:
                self.push_back(bool(b))

    def push_back(self, value: bool):
        if self._size & 7 == 0:
            self._data.append(0)
        if value:
            self._data[self._size >> 3] |= (1 << (self._size & 7))
        self._size += 1

    def __getitem__(self, i):
        if i < 0: i += self._size
        if not (0 <= i < self._size): raise IndexError()
        return bool(self._data[i >> 3] & (1 << (i & 7)))

    def __setitem__(self, i, v: bool):
        if i < 0: i += self._size
        if not (0 <= i < self._size): raise IndexError()
        byte_idx = i >> 3
        bit = i & 7
        if v:
            self._data[byte_idx] |= (1 << bit)
        else:
            self._data[byte_idx] &= ~(1 << bit)

    def __len__(self): return self._size
    def __iter__(self):
        for i in range(self._size):
            yield self[i]

    def __repr__(self):
        return f"vector<bool>[{self._size}] bits={self._size} bytes={len(self._data)} {list(self)[:20]}{'...' if len(self)>20 else ''}"


# =================================================================
# 3. NumericVector — 100% NumPy zero-copy compatible
# =================================================================
class NumericVector:
    """Blazing fast vector for int/float with full NumPy interop"""
    __slots__ = ('array',)

    def __init__(self, data=None, dtype='q'):  # 'q' = int64, 'd' = double
        self.array = array.array(dtype)
        if data:
            self.array.extend(data)

    def push_back(self, x):
        self.array.append(x)

    def __getitem__(self, i):
        return self.array[i]

    def __setitem__(self, i, v):
        self.array[i] = v

    def __len__(self):
        return len(self.array)

    def __buffer__(self, flags):
        return memoryview(self.array)

    def __repr__(self):
        return f"NumericVector[{len(self)}] {list(self.array)}"