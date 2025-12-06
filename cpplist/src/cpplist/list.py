from __future__ import annotations
from typing import TypeVar, Generic, Iterable, Iterator, Any
import sys

T = TypeVar('T')

class ListNode(Generic[T]):
    __slots__ = ('value', 'prev', 'next')
    
    def __init__(self, value: T, prev: ListNode[T] | None = None, next: ListNode[T] | None = None):
        self.value = value
        self.prev = prev
        self.next = next

from cppbase import Sequence

class List(Sequence, Generic[T]):
    __slots__ = ('_head', '_tail', '_size')

    def __init__(self, source: Iterable[T] | None = None):
        self._head: ListNode[T] | None = None
        self._tail: ListNode[T] | None = None
        self._size = 0
        if source is not None:
            self.assign(source)

    # --------------------- Modifiers ---------------------
    def assign(self, source: Iterable[T] | int, value: T | None = None):
        self.clear()
        if isinstance(source, int):
            for _ in range(source):
                self.push_back(value if value is not None else None) # type: ignore
        else:
            for x in source:
                self.push_back(x)

    def push_back(self, value: T):
        new_node = ListNode(value, prev=self._tail, next=None)
        if self._tail:
            self._tail.next = new_node
        self._tail = new_node
        if not self._head:
            self._head = new_node
        self._size += 1

    def push_front(self, value: T):
        new_node = ListNode(value, prev=None, next=self._head)
        if self._head:
            self._head.prev = new_node
        self._head = new_node
        if not self._tail:
            self._tail = new_node
        self._size += 1

    def pop_back(self) -> T:
        if not self._tail:
            raise IndexError("pop_back from empty list")
        val = self._tail.value
        prev_node = self._tail.prev
        if prev_node:
            prev_node.next = None
            self._tail = prev_node
        else:
            self._head = None
            self._tail = None
        self._size -= 1
        return val

    def pop_front(self) -> T:
        if not self._head:
            raise IndexError("pop_front from empty list")
        val = self._head.value
        next_node = self._head.next
        if next_node:
            next_node.prev = None
            self._head = next_node
        else:
            self._head = None
            self._tail = None
        self._size -= 1
        return val

    def clear(self):
        # In Python, clearing references is enough for GC
        # strict C++ might iterate and destroy, but here we just detach
        self._head = None
        self._tail = None
        self._size = 0

    def insert(self, index: int, value: T):
        if index < 0: index += self._size
        if index > self._size: # allow appending at end
             index = self._size
        if index < 0: index = 0 # strict clamp? C++ usually UB or iter based. Here we accept indices.
        
        if index == 0:
            self.push_front(value)
            return
        if index == self._size:
            self.push_back(value)
            return
            
        # Find node
        # Optimization: traverse from closest end
        if index < self._size // 2:
            curr = self._head
            for _ in range(index):
                curr = curr.next # type: ignore
        else:
            curr = self._tail
            for _ in range(self._size - 1 - index):
                curr = curr.prev # type: ignore
        
        # Insert before curr
        # curr is the node that will be AFTER the new node
        # previous node -> new_node -> curr
        prev_node = curr.prev # type: ignore
        new_node = ListNode(value, prev=prev_node, next=curr)
        if prev_node:
            prev_node.next = new_node
        curr.prev = new_node # type: ignore
        self._size += 1

    def erase(self, index: int):
        if index < 0: index += self._size
        if not (0 <= index < self._size):
            raise IndexError("list erase index out of range")
            
        if index == 0:
            self.pop_front()
            return
        if index == self._size - 1:
            self.pop_back()
            return

        # Optimization: traverse from closest end
        if index < self._size // 2:
            node_to_delete = self._head
            for _ in range(index):
                node_to_delete = node_to_delete.next # type: ignore
        else:
            node_to_delete = self._tail
            for _ in range(self._size - 1 - index):
                node_to_delete = node_to_delete.prev # type: ignore

        prev_node = node_to_delete.prev # type: ignore
        next_node = node_to_delete.next # type: ignore
        
        if prev_node:
            prev_node.next = next_node
        if next_node:
            next_node.prev = prev_node
        
        self._size -= 1
        
    def swap(self, other: 'List'):
        if self is other:
            return
        (self._head, other._head) = (other._head, self._head)
        (self._tail, other._tail) = (other._tail, self._tail)
        (self._size, other._size) = (other._size, self._size)

    # --------------------- Access ---------------------
    def front(self) -> T:
        if not self._head:
            raise IndexError("front on empty list")
        return self._head.value

    def back(self) -> T:
        if not self._tail:
            raise IndexError("back on empty list")
        return self._tail.value
        
    def size(self) -> int: return self._size
    def empty(self) -> bool: return self._size == 0

    def __len__(self): return self._size
    
    def __iter__(self) -> Iterator[T]:
        curr = self._head
        while curr:
            yield curr.value
            curr = curr.next

    def __repr__(self):
        data = ', '.join(repr(x) for x in self)
        return f"List[{self._size}]({data})"

    # --------------------- Comparisons ---------------------
    def __eq__(self, other): return list(self) == list(other)
    def __ne__(self, other): return not (self == other)
    def __lt__(self, other): return list(self) < list(other)
    def __le__(self, other): return list(self) <= list(other)
    def __gt__(self, other): return list(self) > list(other)
    def __ge__(self, other): return list(self) >= list(other)
