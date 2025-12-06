from __future__ import annotations
from typing import TypeVar, Generic, Sequence, Iterator, Any, overload
from cppbase import Sequence as BaseSequence

T = TypeVar('T')

class Span(BaseSequence, Generic[T]):
    """
    A Python implementation of C++ std::span.
    Top-level view over a contiguous sequence (list, array, tuple, vector, etc.).
    Does not own the data.
    """
    __slots__ = ('_data', '_offset', '_count')

    def __init__(self, data: Any, offset: int = 0, count: int = -1):
        """
        Construct a Span from a container or another Span.
        
        Args:
            data: The source container (Sequence) or another Span.
            offset: Start index in the source.
            count: Number of elements. -1 means "until the end".
        """
        # Unwrap if data is already a Span to avoid nesting chains
        if isinstance(data, Span):
            self._data = data._data
            base_offset = data._offset
            base_count = data._count
            
            # Validate and adjust bounds relative to the parent Span
            if offset < 0: offset = 0
            if offset > base_count: 
                raise IndexError(f"Span offset {offset} out of range for source span of size {base_count}")
            
            self._offset = base_offset + offset
            max_available = base_count - offset
        else:
            self._data = data
            container_len = len(data)
            
            if offset < 0: offset = 0
            if offset > container_len:
                raise IndexError(f"Span offset {offset} out of range for container of size {container_len}")
                
            self._offset = offset
            max_available = container_len - offset

        if count == -1:
            self._count = max_available
        else:
            if count > max_available:
                raise IndexError(f"Span count {count} exceeds available elements {max_available}")
            self._count = count

    # --------------------- Iteration ---------------------
    def __iter__(self) -> Iterator[T]:
        # Iterate over the virtual slice
        for i in range(self._count):
            yield self._data[self._offset + i]

    def __len__(self) -> int:
        return self._count

    # --------------------- Access ---------------------
    def __getitem__(self, index: int | slice) -> T | Span[T]:
        if isinstance(index, slice):
            start, stop, step = index.indices(self._count)
            if step != 1:
                raise ValueError("Span currently supports only contiguous slicing (step=1)")
            return Span(self._data, self._offset + start, stop - start)
        
        if index < 0: index += self._count
        if not (0 <= index < self._count):
            raise IndexError("Span index out of range")
        return self._data[self._offset + index]

    def __setitem__(self, index: int, value: T):
        if index < 0: index += self._count
        if not (0 <= index < self._count):
            raise IndexError("Span index out of range")
        self._data[self._offset + index] = value

    def front(self) -> T:
        if self._count == 0: raise IndexError("front() on empty Span")
        return self[0]

    def back(self) -> T:
        if self._count == 0: raise IndexError("back() on empty Span")
        return self[self._count - 1]

    def data(self) -> Any:
        # Best effort return of underlying data structure
        return self._data

    # --------------------- Capacity ---------------------
    def size(self) -> int: return self._count
    def empty(self) -> bool: return self._count == 0
    def size_bytes(self) -> int:
        raise NotImplementedError("size_bytes() not supported in generic Python Span")

    # --------------------- Operations ---------------------
    def subspan(self, offset: int, count: int = -1) -> Span[T]:
        return Span(self, offset, count)

    def first(self, count: int) -> Span[T]:
        return self.subspan(0, count)

    def last(self, count: int) -> Span[T]:
        return self.subspan(self._count - count, count)
    
    def __repr__(self):
        # Preview first few elements
        limit = 10
        items_str = []
        for i in range(min(self._count, limit)):
            items_str.append(repr(self[i]))
        if self._count > limit:
            items_str.append("...")
        return f"Span([{', '.join(items_str)}], size={self._count})"
