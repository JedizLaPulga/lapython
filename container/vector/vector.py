from __future__ import annotations
from typing import TypeVar, Generic, Iterable, Any, overload
import ctypes

T = TypeVar('T')

class Vector(Generic[T]):
    """The ultimate Python mimic of C++ std::vector<T>"""
    
    def __init__(self, capacity: int = 0):
        self._size = 0
        self._capacity = 0
        self._data = None
        if capacity > 0:
            self.reserve(capacity)

    # ==================== Capacity ====================
    def size(self) -> int:
        return self._size

    def capacity(self) -> int:
        return self._capacity

    def empty(self) -> bool:
        return self._size == 0

    def reserve(self, new_capacity: int) -> None:
        if new_capacity > self._capacity:
            self._resize(new_capacity)

    def shrink_to_fit(self) -> None:
        if self._size < self._capacity:
            self._resize(self._size)

    def resize(self, new_size: int, value: T | None = None) -> None:
        if new_size > self._size:
            self.reserve(new_size)
            for i in range(self._size, new_size):
                self._data[i] = value if value is not None else None
        self._size = new_size

    # ==================== Element Access ====================
    def front(self) -> T:
        if self._size == 0: raise IndexError("front() on empty vector")
        return self._data[0]

    def back(self) -> T:
        if self._size == 0: raise IndexError("back() on empty vector")
        return self._data[self._size - 1]

    def at(self, index: int) -> T:
        if index < 0: index += self._size
        if index < 0 or index >= self._size:
            raise IndexError("vector::at() index out of range")
        return self._data[index]

    def data(self):
        """Return a memoryview of the underlying array (like C++ data())"""
        if self._data is None:
            return memoryview(bytearray())
        return memoryview(self._data)

    @overload
    def __getitem__(self, index: int) -> T: ...
    @overload
    def __getitem__(self, s: slice) -> list[T]: ...
    def __getitem__(self, key):
        if isinstance(key, slice):
            return [self[i] for i in range(*key.indices(self._size))]
        if key < 0: key += self._size
        if not (0 <= key < self._size):
            raise IndexError("vector index out of range")
        return self._data[key]

    def __setitem__(self, index: int, value: T) -> None:
        if index < 0: index += self._size
        if not (0 <= index < self._size):
            raise IndexError("vector assignment index out of range")
        self._data[index] = value

    # ==================== Modifiers ====================
    def push_back(self, value: T) -> None:
        if self._size == self._capacity:
            self._resize(max(1, self._capacity * 2))
        self._data[self._size] = value
        self._size += 1

    def emplace_back(self, *args: Any) -> T:
        """Construct element in-place (simulated)"""
        if self._size == self._capacity:
            self._resize(max(1, self._capacity * 2))
        # Simulate in-place construction via the type's __new__
        obj = object.__new__(args[0]) if args and hasattr(args[0], '__new__') else None
        if len(args) == 1 and not isinstance(args[0], type):
            obj = args[0]
        elif args:
            obj.__init__(*args[1:]) if hasattr(obj, '__init__') else None
        self._data[self._size] = obj
        self._size += 1
        return obj

    def pop_back(self) -> T:
        if self._size == 0:
            raise IndexError("pop_back from empty vector")
        self._size -= 1
        value = self._data[self._size]
        self._data[self._size] = None
        return value

    def insert(self, index: int, value: T) -> None:
        if index < 0: index += self._size
        if not (0 <= index <= self._size):
            raise IndexError("insert index out of range")
        if self._size == self._capacity:
            self._resize(max(1, self._capacity * 2))
        for i in range(self._size, index, -1):
            self._data[i] = self._data[i-1]
        self._data[index] = value
        self._size += 1

    def erase(self, first: int, last: int | None = None) -> None:
        if first < 0: first += self._size
        if last is None: last = first + 1
        if last < 0: last += self._size
        if not (0 <= first <= last <= self._size):
            raise IndexError("erase range out of bounds")
        count = last - first
        for i in range(first, self._size - count):
            self._data[i] = self._data[i + count]
        self._size -= count
        for i in range(self._size, self._size + count):
            self._data[i] = None

    def clear(self) -> None:
        self._size = 0

    # ==================== Iterators ====================
    def begin(self):
        return VectorIterator(self, 0)

    def end(self):
        return VectorIterator(self, self._size)

    def __iter__(self):
        return VectorIterator(self, 0)

    # ==================== Utilities ====================
    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        content = ', '.join(repr(x) for x in self)
        return f"Vector[{self._size}/{self._capacity}]({content})"

    def __bool__(self) -> bool:
        return self._size > 0

    # Internal resize
    def _resize(self, new_capacity: int) -> None:
        new_capacity = max(new_capacity, self._size)
        if new_capacity == self._capacity:
            return
        # Use array.array or ctypes for real contiguous memory if you want max speed
        new_data = (ctypes.py_object * new_capacity)()
        for i in range(self._size):
            new_data[i] = self._data[i] if self._data else None
        self._data = new_data
        self._capacity = new_capacity


class VectorIterator:
    def __init__(self, vector: Vector, index: int):
        self.vector = vector
        self.index = index

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= self.vector.size():
            raise StopIteration
        value = self.vector[self.index]
        self.index += 1
        return value

    def __add__(self, n: int):
        return VectorIterator(self.vector, self.index + n)

    def __sub__(self, n: int):
        return VectorIterator(self.vector, self.index - n)