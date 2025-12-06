from __future__ import annotations
from typing import TypeVar, Generic, Any, Protocol

T = TypeVar('T')

class ContainerProtocol(Protocol):
    def push_back(self, value: Any) -> None: ...
    def pop_front(self) -> Any: ...
    def front(self) -> Any: ...
    def back(self) -> Any: ...
    def empty(self) -> bool: ...
    def size(self) -> int: ...

class Queue(Generic[T]):
    __slots__ = ('c',)

    def __init__(self, container: Any | None = None):
        """
        A standard C++ style Queue adapter.
        
        Args:
            container: The underlying container to use. 
                       Must support push_back, pop_front, front, back, empty, size.
                       If None, defaults to a simple list wrapper (or expected user to provide one).
                       In strict C++, this defaults to std::deque.
        """
        if container is None:
            # Fallback to a simple list-based wrapper if nothing provided, 
            # though usually you'd want cppdeque.
            self.c = _ListContainer()
        else:
            self.c = container

    def push(self, value: T):
        """Inserts element at the end."""
        self.c.push_back(value)

    def pop(self):
        """Removes the next element."""
        self.c.pop_front()

    def front(self) -> T:
        """Access the next element."""
        return self.c.front()

    def back(self) -> T:
        """Access the last element."""
        return self.c.back()

    def empty(self) -> bool:
        """Checks whether the underlying container is empty."""
        return self.c.empty()

    def size(self) -> int:
        """Returns the number of elements."""
        return self.c.size()
    
    def __len__(self) -> int:
        return self.size()

    def __repr__(self):
        return f"Queue(wrapping {self.c})"

# A simple valid container implementation using Python list
# Used as default if user doesn't pass a cppdeque/cpplist
class _ListContainer:
    def __init__(self):
        self._data = []
    def push_back(self, x): self._data.append(x)
    def pop_front(self): 
        if not self._data: raise IndexError("empty")
        return self._data.pop(0)
    def front(self): return self._data[0]
    def back(self): return self._data[-1]
    def empty(self): return not self._data
    def size(self): return len(self._data)
    def __repr__(self): return repr(self._data)
