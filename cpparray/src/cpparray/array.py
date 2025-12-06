from __future__ import annotations
from typing import TypeVar, Generic, Iterable, Iterator, Any, Sequence, overload
import ctypes

T = TypeVar('T')

class Array(Generic[T]):
    __slots__ = ('_data', '_size')

    def __init__(self, size: int, init_value: T | None = None, source: Iterable[T] | None = None):
        """
        Fixed-size array implementation similar to std::array<T, N>.
        
        Args:
            size: The fixed size N of the array.
            init_value: Value to fill the array with if source is insufficient.
            source: Iterable to initialize the array.
        """
        if size < 0:
            raise ValueError("Array size cannot be negative")
            
        self._size = size
        # Create a fixed-size array of python objects
        self._data = (ctypes.py_object * size)()
        
        # Initialize
        if source is not None:
            # Fill from source
            i = 0
            for x in source:
                if i >= size:
                    raise IndexError("Initializer list too long for Array size")
                self._data[i] = x
                i += 1
            # Fill remainder with init_value
            while i < size:
                self._data[i] = init_value
                i += 1
        else:
            # Fill all with init_value
            for i in range(size):
                self._data[i] = init_value

    # --------------------- Element Access ---------------------
    def at(self, pos: int) -> T:
        """Access element with bounds checking."""
        if pos < 0 or pos >= self._size:
            raise IndexError("Array::at index out of range")
        return self._data[pos]

    def __getitem__(self, pos: int) -> T:
        if pos < 0: pos += self._size
        if not (0 <= pos < self._size):
            raise IndexError("Array index out of range")
        return self._data[pos]

    def __setitem__(self, pos: int, value: T):
        if pos < 0: pos += self._size
        if not (0 <= pos < self._size):
            raise IndexError("Array index out of range")
        self._data[pos] = value

    def front(self) -> T:
        if self._size == 0: raise IndexError("front() called on empty Array")
        return self._data[0]

    def back(self) -> T:
        if self._size == 0: raise IndexError("back() called on empty Array")
        return self._data[self._size - 1]

    def data(self) -> ctypes.Array:
        """Returns the underlying ctypes (raw) array."""
        return self._data

    # --------------------- Capacity ---------------------
    def empty(self) -> bool:
        return self._size == 0

    def size(self) -> int:
        return self._size

    def max_size(self) -> int:
        return self._size

    def __len__(self) -> int:
        return self._size

    # --------------------- Operations ---------------------
    def fill(self, value: T):
        """Assigns the given value to every element in the array."""
        for i in range(self._size):
            self._data[i] = value

    def swap(self, other: 'Array[T]'):
        """Exchanges the contents of the container with those of other."""
        if not isinstance(other, Array):
            raise TypeError("Can only swap with another Array")
        if self._size != other._size:
            raise ValueError("Can only swap Arrays of the same size") # C++ std::array swap requires strict type (same N)
        
        # Efficient swap of internal pointer
        # Note: In C++ strict terms, std::array swap is linear. 
        # But in Python, swapping the backing storage object is safe and O(1).
        self._data, other._data = other._data, self._data

    # --------------------- Iterators ---------------------
    def __iter__(self) -> Iterator[T]:
        for i in range(self._size):
            yield self._data[i]

    def __repr__(self):
        # Prevent huge output for large arrays
        if self._size > 20:
            preview = list(self._data[:10])
            return f"Array[{self._size}]({preview} ...)"
        return f"Array[{self._size}]({list(self)})"

    # --------------------- Comparisons ---------------------
    def __eq__(self, other): 
        if not isinstance(other, Array) or self._size != other._size:
            return False
        # Element-wise comparison
        for i in range(self._size):
            if self._data[i] != other._data[i]:
                return False
        return True
