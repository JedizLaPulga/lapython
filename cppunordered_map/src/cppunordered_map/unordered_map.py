from __future__ import annotations
from typing import TypeVar, Generic, Tuple, Iterator, Any, List

K = TypeVar('K')
V = TypeVar('V')

class _HashNode(Generic[K, V]):
    __slots__ = ('key', 'value', 'next')
    def __init__(self, key: K, value: V, next_node: _HashNode[K,V] | None = None):
        self.key = key
        self.value = value
        self.next = next_node

class UnorderedMap(Generic[K, V]):
    __slots__ = ('_buckets', '_size', '_bucket_count', '_max_load_factor')
    
    # std::unordered_map implementation using Separate Chaining (buckets)
    # Python's dict is open addressing (optimized).
    # We implement separate chaining to behave strictly like typical C++ std implementations (e.g. GCC libstdc++).
    # This exposes "bucket interface" which is part of the STL standard.

    def __init__(self, source=None, bucket_count: int = 8):
        self._bucket_count = bucket_count
        self._buckets: List[_HashNode[K,V] | None] = [None] * bucket_count
        self._size = 0
        self._max_load_factor = 1.0 # Standard default
        
        if source:
            if isinstance(source, dict):
                for k, v in source.items():
                    self[k] = v
            else:
                for k, v in source:
                    self[k] = v

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
                self[curr.key] = curr.value # Re-insert
                curr = curr.next

    # --------------------- Modifiers ---------------------
    def __setitem__(self, key: K, value: V):
        idx = self._hash(key)
        head = self._buckets[idx]
        
        # Check update
        curr = head
        while curr:
            if curr.key == key:
                curr.value = value
                return
            curr = curr.next
            
        # Insert new
        new_node = _HashNode(key, value, head)
        self._buckets[idx] = new_node
        self._size += 1
        
        # Load factor check
        if self.load_factor() > self._max_load_factor:
            self._rehash(self._bucket_count * 2)

    def insert(self, key: K, value: V):
        self[key] = value

    def erase(self, key: K):
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
        # Else not found (no-op in C++ erase(key) returns 0)

    # --------------------- Access ---------------------
    def __getitem__(self, key: K) -> V:
        idx = self._hash(key)
        curr = self._buckets[idx]
        while curr:
            if curr.key == key:
                return curr.value
            curr = curr.next
        raise KeyError(key)

    def find(self, key: K) -> Any | None:
        try:
            return self[key]
        except KeyError:
            return None

    def count(self, key: K) -> int:
        return 1 if self.find(key) is not None else 0

    # --------------------- Buckets (Unique to unordered containers) ---------------------
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
        items = ", ".join(f"{k!r}: {v!r}" for k, v in self.items())
        return f"UnorderedMap({{{items}}})"

    def size(self): return self._size
    def empty(self): return self._size == 0
    def __len__(self): return self._size
