from typing import TypeVar, Generic, Iterable, Iterator, Any, List, Optional
from cppbase import Associative
import bisect

T = TypeVar('T')

class FlatSet(Associative, Generic[T]):
    """
    A Python implementation of C++23 std::flat_set.
    
    A sorted associative container that contains unique keys.
    Keys are stored in a sorted underlying sequence (list).
    
    Search is O(log N).
    Insertion/Erasure is O(N).
    """
    __slots__ = ('_data')

    def __init__(self, data: Optional[Iterable[T]] = None):
        self._data: List[T] = []
        
        if data:
            # Sort and deduplicate
            # Sort O(N log N)
            sorted_data = sorted(data)
            
            # Unique O(N)
            if sorted_data:
                self._data.append(sorted_data[0])
                for i in range(1, len(sorted_data)):
                    if sorted_data[i] != sorted_data[i-1]:
                        self._data.append(sorted_data[i])

    # --------------------- Capacity ---------------------
    def empty(self) -> bool:
        return len(self._data) == 0

    def size(self) -> int:
        return len(self._data)
    
    def max_size(self) -> int:
        return 9223372036854775807

    # --------------------- Iteration ---------------------
    def __iter__(self) -> Iterator[T]:
        return iter(self._data)
    
    def begin(self) -> Iterator[T]:
        return iter(self._data)

    def end(self):
        pass

    # --------------------- Access & Modifiers ---------------------
    def insert(self, value: T) -> bool:
        """
        Inserts element if not present.
        Returns True if inserted, False if already present.
        """
        idx = bisect.bisect_left(self._data, value)
        if idx < len(self._data) and self._data[idx] == value:
            return False
        self._data.insert(idx, value)
        return True
        
    def erase(self, value: T) -> int:
        """Removes the element. Returns 1 if removed, 0 if not found."""
        idx = bisect.bisect_left(self._data, value)
        if idx < len(self._data) and self._data[idx] == value:
            del self._data[idx]
            return 1
        return 0

    def clear(self):
        self._data.clear()

    def swap(self, other: 'FlatSet[T]'):
        self._data, other._data = other._data, self._data

    # --------------------- Lookup ---------------------
    def count(self, value: T) -> int:
        idx = bisect.bisect_left(self._data, value)
        if idx < len(self._data) and self._data[idx] == value:
            return 1
        return 0
        
    def find(self, value: T) -> Iterator[T]:
        idx = bisect.bisect_left(self._data, value)
        if idx < len(self._data) and self._data[idx] == value:
            yield self._data[idx]

    def contains(self, value: T) -> bool:
        return self.count(value) > 0

    def lower_bound(self, value: T) -> int:
        return bisect.bisect_left(self._data, value)

    def upper_bound(self, value: T) -> int:
        return bisect.bisect_right(self._data, value)

    # --------------------- Operations ---------------------
    def __repr__(self) -> str:
        return f"FlatSet([{', '.join(map(str, self._data))}])"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FlatSet):
            return NotImplemented
        return self._data == other._data
