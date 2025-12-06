from __future__ import annotations
from typing import TypeVar, Generic, Iterator, Any, List
from cppbase import Unordered

T = TypeVar('T')

class _HashNode(Generic[T]):
    __slots__ = ('key', 'next')
    def __init__(self, key: T, next_node: _HashNode[T] | None = None):
        self.key = key
        self.next = next_node

class UnorderedMultiSet(Unordered, Generic[T]):
    __slots__ = ('_buckets', '_size', '_bucket_count', '_max_load_factor')
    
    def __init__(self, source=None, bucket_count: int = 8):
        self._bucket_count = bucket_count
        self._buckets: List[_HashNode[T] | None] = [None] * bucket_count
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
                self.insert(curr.key)
                curr = curr.next

    # --------------------- Modifiers ---------------------
    def insert(self, key: T):
        idx = self._hash(key)
        head = self._buckets[idx]
        new_node = _HashNode(key, head)
        self._buckets[idx] = new_node
        self._size += 1
        
        if self.load_factor() > self._max_load_factor:
            self._rehash(self._bucket_count * 2)

    def erase(self, key: T) -> int:
        idx = self._hash(key)
        head = self._buckets[idx]
        
        count = 0
        prev = None
        curr = head
        while curr:
            if curr.key == key:
                count += 1
                self._size -= 1
                if prev:
                    prev.next = curr.next
                else:
                    head = curr.next
                curr = curr.next
            else:
                prev = curr
                curr = curr.next
        
        self._buckets[idx] = head
        return count

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

    def count(self, key: T) -> int:
        idx = self._hash(key)
        curr = self._buckets[idx]
        c = 0
        while curr:
            if curr.key == key:
                c += 1
            curr = curr.next
        return c
    
    def contains(self, key: T) -> bool:
        return self.find(key) is not None

    def bucket_count(self) -> int: return self._bucket_count
    def load_factor(self) -> float: return self._size / self._bucket_count
    def __len__(self) -> int: return self._size
    def empty(self) -> bool: return self._size == 0
    def size(self) -> int: return self._size

    # --------------------- Iteration ---------------------
    def __iter__(self) -> Iterator[T]:
        for head in self._buckets:
            curr = head
            while curr:
                yield curr.key
                curr = curr.next

    def __repr__(self):
        return f"UnorderedMultiSet({{{', '.join(repr(x) for x in self)}}})"
