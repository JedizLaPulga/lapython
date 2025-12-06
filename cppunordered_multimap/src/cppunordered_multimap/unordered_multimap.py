from __future__ import annotations
from typing import TypeVar, Generic, Tuple, Iterator, Any, List
from cppbase import Unordered

K = TypeVar('K')
V = TypeVar('V')

class _HashNode(Generic[K, V]):
    __slots__ = ('key', 'value', 'next')
    def __init__(self, key: K, value: V, next_node: _HashNode[K,V] | None = None):
        self.key = key
        self.value = value
        self.next = next_node

class UnorderedMultiMap(Unordered, Generic[K, V]):
    __slots__ = ('_buckets', '_size', '_bucket_count', '_max_load_factor')
    
    def __init__(self, source=None, bucket_count: int = 8):
        self._bucket_count = bucket_count
        self._buckets: List[_HashNode[K,V] | None] = [None] * bucket_count
        self._size = 0
        self._max_load_factor = 1.0
        
        if source:
            if isinstance(source, dict):
                for k, v in source.items():
                    self.insert(k, v)
            else:
                for k, v in source:
                    self.insert(k, v)

    def _hash(self, key: K) -> int:
        return hash(key) % self._bucket_count

    def _rehash(self, new_count: int):
        old_buckets = self._buckets
        self._bucket_count = new_count
        self._buckets = [None] * new_count
        self._size = 0
        
        for head in old_buckets:
            curr = head
            while curr:
                self.insert(curr.key, curr.value)
                curr = curr.next

    def insert(self, key: K, value: V):
        idx = self._hash(key)
        head = self._buckets[idx]
        new_node = _HashNode(key, value, head)
        self._buckets[idx] = new_node
        self._size += 1
        
        if self.load_factor() > self._max_load_factor:
            self._rehash(self._bucket_count * 2)

    def erase(self, key: K) -> int:
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
                # Do NOT advance prev here, because curr is now a new node (the old curr.next)
            else:
                prev = curr
                curr = curr.next
        
        self._buckets[idx] = head
        return count

    def clear(self):
        self._buckets = [None] * self._bucket_count
        self._size = 0

    def find(self, key: K) -> Iterator[Tuple[K,V]] | None:
        idx = self._hash(key)
        curr = self._buckets[idx]
        while curr:
            if curr.key == key:
                return (curr.key, curr.value)
            curr = curr.next
        return None

    def count(self, key: K) -> int:
        idx = self._hash(key)
        curr = self._buckets[idx]
        c = 0
        while curr:
            if curr.key == key:
                c += 1
            curr = curr.next
        return c

    def equal_range(self, key: K) -> Iterator[Tuple[K,V]]:
        idx = self._hash(key)
        curr = self._buckets[idx]
        while curr:
            if curr.key == key:
                yield (curr.key, curr.value)
            curr = curr.next

    def bucket_count(self) -> int: return self._bucket_count
    def load_factor(self) -> float: return self._size / self._bucket_count
    def __len__(self) -> int: return self._size
    def empty(self) -> bool: return self._size == 0
    def size(self) -> int: return self._size

    def __iter__(self):
        for head in self._buckets:
            curr = head
            while curr:
                yield curr.key
                curr = curr.next

    def items(self) -> Iterator[Tuple[K, V]]:
        for head in self._buckets:
            curr = head
            while curr:
                yield (curr.key, curr.value)
                curr = curr.next

    def __repr__(self):
        return f"UnorderedMultiMap({{{', '.join(f'{k!r}: {v!r}' for k, v in self.items())}}})"
