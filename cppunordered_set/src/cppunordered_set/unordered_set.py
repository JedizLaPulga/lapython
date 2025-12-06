from __future__ import annotations
from typing import TypeVar, Generic, Iterator, Any, List

T = TypeVar('T')

class _SetNode(Generic[T]):
    __slots__ = ('key', 'next')
    def __init__(self, key: T, next_node: _SetNode[T] | None = None):
        self.key = key
        self.next = next_node

from cppbase import Unordered

class UnorderedSet(Unordered, Generic[T]):
    __slots__ = ('_buckets', '_size', '_bucket_count', '_max_load_factor')
    
    # std::unordered_set implementation (Hash Set with Buckets)
    # Similar to unordered_map but stores only keys.

    def __init__(self, source=None, bucket_count: int = 8):
        self._bucket_count = bucket_count
        self._buckets: List[_SetNode[T] | None] = [None] * bucket_count
        self._size = 0
        self._max_load_factor = 1.0
        
        if source:
            for x in source:
                self.insert(x)

    def _hash(self, key: T) -> int:
        return hash(key) % self._bucket_count

    def _rehash(self, new_count: int):
        old_buckets = self._buckets
        self._bucket_count = new_count
        self._buckets = [None] * new_count
        self._size = 0
        
        for head in old_buckets:
            curr = head
            while curr:
                self.insert(curr.key) # Re-insert (recurses but handles new size)
                # Wait, calling insert() triggers size++ and potential recursive loop if not careful?
                # Actually, standard insert() increments size. 
                # Better implementation: manual re-insertion to avoid size increment logic issues or just reset size.
                # Here we reset size=0 above, so calling insert matches.
                # EFFICIENCY: calling insert recalc hash. Correct.
                curr = curr.next

    # --------------------- Modifiers ---------------------
    def insert(self, key: T):
        idx = self._hash(key)
        head = self._buckets[idx]
        
        # Check if exists
        curr = head
        while curr:
            if curr.key == key:
                return # Unique keys only
            curr = curr.next
            
        # Insert new
        new_node = _SetNode(key, head)
        self._buckets[idx] = new_node
        self._size += 1
        
        if self.load_factor() > self._max_load_factor:
            self._rehash(self._bucket_count * 2)

    def erase(self, key: T):
        idx = self._hash(key)
        head = self._buckets[idx]
        
        prev = None
        curr = head
        while curr:
            if curr.key == key:
                if prev:
                    prev.next = curr.next
                else:
                    self._buckets[idx] = curr.next
                self._size -= 1
                return
            prev = curr
            curr = curr.next

    def clear(self):
        self._buckets = [None] * self._bucket_count
        self._size = 0

    # --------------------- Access ---------------------
    def find(self, key: T) -> T | None:
        idx = self._hash(key)
        curr = self._buckets[idx]
        while curr:
            if curr.key == key:
                return curr.key
            curr = curr.next
        return None

    def contains(self, key: T) -> bool:
        return self.find(key) is not None

    def count(self, key: T) -> int:
        return 1 if self.contains(key) else 0

    # --------------------- Buckets ---------------------
    def bucket_count(self) -> int:
        return self._bucket_count

    def load_factor(self) -> float:
        return self._size / self._bucket_count

    def max_load_factor(self, z: float | None = None) -> float:
        if z is not None:
            self._max_load_factor = z
        return self._max_load_factor

    def bucket_size(self, n: int) -> int:
        if n >= self._bucket_count: return 0
        count = 0
        curr = self._buckets[n]
        while curr:
            count += 1
            curr = curr.next
        return count

    # --------------------- Iteration ---------------------
    def __iter__(self) -> Iterator[T]:
        for head in self._buckets:
            curr = head
            while curr:
                yield curr.key
                curr = curr.next

    def __repr__(self):
        return f"UnorderedSet({{{', '.join(repr(x) for x in self)}}})"

    def size(self): return self._size
    def empty(self): return self._size == 0
    def __len__(self): return self._size
