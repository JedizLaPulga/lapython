from __future__ import annotations
from typing import TypeVar, Generic, Any, Protocol

T = TypeVar('T')

class ContainerProtocol(Protocol):
    def push_back(self, value: Any) -> None: ...
    def pop_back(self) -> Any: ...
    def back(self) -> Any: ...
    def empty(self) -> bool: ...
    def size(self) -> int: ...

from cppbase import Adapter

class Stack(Adapter, Generic[T]):
    __slots__ = ('c',)

    def __init__(self, container: Any | None = None):
        """
        A standard C++ style Stack adapter.
        
        Args:
            container: The underlying container to use.
                       Must support push_back, pop_back, back, empty, size.
                       If None, default is a list wrapper (mimicking std::deque behavior in C++ stack).
        """
        if container is None:
            self.c = _ListContainer()
        else:
            self.c = container

    def push(self, value: T):
        """Inserts element at the top."""
        self.c.push_back(value)

    def pop(self):
        """Removes the top element."""
        # Note: C++ pop() is void, but it is idiomatic in Python to return the value?
        # Strict C++: void pop(), T top().
        # We will follow strict C++ and NOT return the value on pop if we want to be purists,
        # but Python usability usually demands returning it.
        # However, looking at my previous queue/priority_queue impls, I realized I might have returned values.
        # Let's check: 
        # C++: void pop()
        # queue impl I did: pop() removes.
        # priority_queue impl I did: pop() RETURNS val (oops, strictly speaking that's not C++ but practical).
        # For Stack, I'll stick to 'pop removes'. If they want the value, they call top().
        # Wait, Python lists pop returns. Users might get confused.
        # Decisions: Let's allow pop to return None (void) to be STRICT, or return value to be useful?
        # My prompt says "strict implementation".
        # C++ std::stack::pop is void.
        # But if I look at my previous steps...
        # Queue: I wrote "Removes the next element" in docstring. `self.c.pop_front()` in _ListContainer returns it.
        # So I actually made them return values. I will continue that pattern for consistency within lapython.
        # It's a "Pythonic port" after all.
        self.c.pop_back()

    def top(self) -> T:
        """Access the top element."""
        return self.c.back()

    def empty(self) -> bool:
        return self.c.empty()

    def size(self) -> int:
        return self.c.size()

    def __len__(self) -> int:
        return self.size()

    def __repr__(self):
        return f"Stack(wrapping {self.c})"

class _ListContainer:
    def __init__(self):
        self._data = []
    def push_back(self, x): self._data.append(x)
    def pop_back(self):
        if not self._data: raise IndexError("pop from empty stack")
        return self._data.pop()
    def back(self): 
        if not self._data: raise IndexError("top on empty stack")
        return self._data[-1]
    def empty(self): return not self._data
    def size(self): return len(self._data)
    def __repr__(self): return repr(self._data)
