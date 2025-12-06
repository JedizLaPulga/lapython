from __future__ import annotations
from typing import TypeVar, Generic, Iterator, Any, List, overload
from cppbase import Sequence

T = TypeVar('T')

class InplaceVector(Sequence, Generic[T]):
    """
    A Python implementation of C++26 std::inplace_vector.
    A dynamically-resizable vector with fixed maximum capacity.
    Does not allocate memory on insertion (storage is pre-allocated).
    """
    __slots__ = ('_data', '_size', '_capacity')

    def __init__(self, capacity: int):
        """
        Initialize with a fixed capacity.
        Args:
            capacity: The maximum number of elements this vector can hold.
        """
        if capacity < 0:
            raise ValueError("Capacity must be non-negative")
        self._capacity = capacity
        # Pre-allocate storage. 
        # In Python, a list of None is efficient enough. 
        # We could use standard vector backing (ctypes) but list is more Pythonic for "slots".
        self._data = [None] * capacity 
        self._size = 0

    # --------------------- Capacity ---------------------
    def size(self) -> int: return self._size
    def max_size(self) -> int: return self._capacity
    def capacity(self) -> int: return self._capacity
    def empty(self) -> bool: return self._size == 0
    
    # --------------------- Modifiers ---------------------
    def push_back(self, value: T):
        """Appends value. Raises MemoryError (bad_alloc) if full."""
        if self._size == self._capacity:
            raise MemoryError("InplaceVector is full (exceeded capacity)")
        self._data[self._size] = value
        self._size += 1

    def pop_back(self):
        """Removes last element."""
        if self._size == 0:
            raise IndexError("pop_back from empty InplaceVector")
        self._size -= 1
        self._data[self._size] = None # Help GC

    def clear(self):
        for i in range(self._size):
            self._data[i] = None
        self._size = 0
        
    def resize(self, n: int, value: T | None = None):
        if n > self._capacity:
            raise MemoryError("resize exceeded capacity")
        if n < self._size:
            # Shrink
            for i in range(n, self._size):
                self._data[i] = None
            self._size = n
        elif n > self._size:
            # Grow
            for i in range(self._size, n):
                self._data[i] = value
            self._size = n

    # --------------------- Access ---------------------
    def __getitem__(self, i: int) -> T:
        if i < 0: i += self._size
        if not (0 <= i < self._size):
            raise IndexError("InplaceVector index out of range")
        return self._data[i]
    
    def __setitem__(self, i: int, value: T):
        if i < 0: i += self._size
        if not (0 <= i < self._size):
            raise IndexError("InplaceVector index out of range")
        self._data[i] = value

    def front(self) -> T:
        if self._size == 0: raise IndexError()
        return self._data[0]

    def back(self) -> T:
        if self._size == 0: raise IndexError()
        return self._data[self._size - 1]

    def try_push_back(self, value: T) -> bool:
        """Returns True if pressed, False if full (no exception)."""
        if self._size == self._capacity:
            return False
        self._data[self._size] = value
        self._size += 1
        return True

    # --------------------- Iteration ---------------------
    def __iter__(self) -> Iterator[T]:
        for i in range(self._size):
            yield self._data[i]
            
    def __len__(self) -> int:
        return self._size

    def __repr__(self):
        # InplaceVector[3/10](1, 2, 3)
        return f"InplaceVector[{self._size}/{self._capacity}]({', '.join(repr(self[i]) for i in range(self._size))})"
