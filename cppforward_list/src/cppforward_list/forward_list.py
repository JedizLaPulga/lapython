from __future__ import annotations
from typing import TypeVar, Generic, Iterable, Iterator, Any

T = TypeVar('T')

class ForwardNode(Generic[T]):
    __slots__ = ('value', 'next')
    
    def __init__(self, value: T, next_node: ForwardNode[T] | None = None):
        self.value = value
        self.next = next_node

from cppbase import Sequence

class ForwardList(Sequence, Generic[T]):
    __slots__ = ('_head', '_size')

    def __init__(self, source: Iterable[T] | None = None):
        """
        std::forward_list implementation (Singly Linked List).
        
        Optimized for memory (1 pointer per node) and fast insertion/removal 
        from the front.
        
        Does NOT support size() in constant time in strict C++11, 
        but we will track it O(1) for Python convenience, 
        as removing it is too painful for Python devs.
        """
        self._head: ForwardNode[T] | None = None
        self._size = 0
        
        if source is not None:
            # push_front reverses order if we just iterate and push.
            # To preserve order, we need to push to back or iterate reversed.
            # Efficient list build: keep tail pointer locally during init.
            tail = None
            for x in source:
                new_node = ForwardNode(x)
                if tail:
                    tail.next = new_node
                else:
                    self._head = new_node
                tail = new_node
                self._size += 1

    # --------------------- Modifiers ---------------------
    def push_front(self, value: T):
        self._head = ForwardNode(value, self._head)
        self._size += 1

    def pop_front(self) -> T:
        if not self._head:
            raise IndexError("pop_front from empty forward_list")
        val = self._head.value
        self._head = self._head.next
        self._size -= 1
        return val

    def insert_after(self, pos_iterator: 'ForwardListIterator', value: T):
        """
        Inserts value AFTER the element pointed to by the iterator.
        This is the standard forward_list way (no insert_before).
        """
        if not pos_iterator.current:
            # If iterator is invalid/end, can't insert after.
            raise ValueError("Iterator is invalid")
        
        node = pos_iterator.current
        new_node = ForwardNode(value, node.next)
        node.next = new_node
        self._size += 1

    def erase_after(self, pos_iterator: 'ForwardListIterator'):
        """
        Removes the element AFTER the element pointed to by iterator.
        """
        if not pos_iterator.current or not pos_iterator.current.next:
            return
        
        node_to_remove = pos_iterator.current.next
        pos_iterator.current.next = node_to_remove.next
        self._size -= 1

    def clear(self):
        self._head = None
        self._size = 0

    def swap(self, other: 'ForwardList'):
        self._head, other._head = other._head, self._head
        self._size, other._size = other._size, self._size

    # --------------------- Access ---------------------
    def front(self) -> T:
        if not self._head:
            raise IndexError("front on empty forward_list")
        return self._head.value

    def empty(self) -> bool:
        return self._head is None

    def max_size(self) -> int:
        return 9223372036854775807 # sys.maxsize

    # --------------------- Operations ---------------------
    def reverse(self):
        # O(N) reverse in-place
        prev = None
        current = self._head
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self._head = prev

    # --------------------- Iterators ---------------------
    def __iter__(self) -> Iterator[T]:
        current = self._head
        while current:
            yield current.value
            current = current.next

    def begin(self) -> 'ForwardListIterator':
        return ForwardListIterator(self._head)

    def before_begin(self) -> 'ForwardListIterator':
        """
        Returns an iterator to a "hypothetical" element before begin.
        Essential for insert_after() at the very start?
        Actually, trickier in Python without sentinel nodes.
        We'll skip before_begin strictness and just rely on push_front for head ops.
        """
        pass

    def __repr__(self):
        # Avoid infinite loop if cyclic (not expected standard usage but possible)
        items = []
        limit = 20
        for x in self:
            items.append(repr(x))
            limit -= 1
            if limit == 0:
                items.append("...")
                break
        return f"ForwardList[{self._size}]({' -> '.join(items)})"

class ForwardListIterator:
    def __init__(self, node: ForwardNode | None):
        self.current = node
    
    def __next__(self):
        if not self.current:
            raise StopIteration
        val = self.current.value
        self.current = self.current.next
        return val
    
    def next(self): # C++ style advance
        if self.current:
            self.current = self.current.next
