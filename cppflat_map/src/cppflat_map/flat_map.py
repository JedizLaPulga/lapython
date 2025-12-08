from typing import TypeVar, Generic, Tuple, Iterator, Any, List, Optional
from cppbase import Associative
import bisect

K = TypeVar('K')
V = TypeVar('V')

class FlatMap(Associative, Generic[K, V]):
    """
    A Python implementation of C++23 std::flat_map.
    
    A sorted associative container that contains key-value pairs with unique keys.
    Keys and values are stored in separate sequences (lists) for cache locality,
    maintained in sorted order by key.
    
    Search is O(log N).
    Insertion/Erasure is O(N).
    """
    __slots__ = ('_keys', '_values')

    def __init__(self, items: Optional[Any] = None):
        """
        Construct a FlatMap.
        
        Args:
            items: Optional list of (key, value) tuples or mapping to initialize with.
                   Note: Bulk initialization sorts the data once (O(N log N)).
        """
        self._keys: List[K] = []
        self._values: List[V] = []
        
        if items:
            if isinstance(items, dict):
                items = items.items()
            
            # Sort items by key to initialize
            sorted_items = sorted(items, key=lambda x: x[0])
            
            # Deduplicate if necessary (std::map semantics usually overwrite or ignore? 
            # C++ range constructor inserts. If unsorted, we sort. 
            # If duplicates, C++ multimap allows, map checks uniqueness.
            # We will assume 'last win' or 'first win'? C++ std::map insert fails if exists.
            # For construction, we'll just build it.)
            
            for k, v in sorted_items:
                # Basic unique check on sorted stream
                if self._keys and self._keys[-1] == k:
                    continue # Skip duplicates (or overwrite? std::map constructor ensures unique)
                self._keys.append(k)
                self._values.append(v)

    # --------------------- Capacity ---------------------
    def empty(self) -> bool:
        return len(self._keys) == 0

    def size(self) -> int:
        return len(self._keys)

    def max_size(self) -> int:
        return 9223372036854775807

    # --------------------- Element Access ---------------------
    def at(self, key: K) -> V:
        """Returns the value associated with the key. Raises KeyError if not found."""
        idx = bisect.bisect_left(self._keys, key)
        if idx < len(self._keys) and self._keys[idx] == key:
            return self._values[idx]
        raise IndexError(f"FlatMap key not found: {key}")

    def __getitem__(self, key: K) -> V:
        try:
            return self.at(key)
        except IndexError:
            # Python dict compatibility
            raise KeyError(key)

    def __setitem__(self, key: K, value: V):
        """Insert or assign (operator[] in C++)."""
        idx = bisect.bisect_left(self._keys, key)
        if idx < len(self._keys) and self._keys[idx] == key:
            self._values[idx] = value
        else:
            self._keys.insert(idx, key)
            self._values.insert(idx, value)

    # --------------------- Iteration ---------------------
    def begin(self) -> Iterator[K]: # Iterating C++ map yields pairs usually, but Python dict yields keys
        return iter(self._keys)

    def end(self):
        # Placeholder for iterator end comparisons
        pass

    def __iter__(self) -> Iterator[K]:
        # Pythonic: iterate keys
        return iter(self._keys)

    def items(self) -> Iterator[Tuple[K, V]]:
        # Helper for key-value iteration
        return zip(self._keys, self._values)

    def keys(self) -> List[K]:
        return self._keys # Return direct reference or copy? List view.

    def values(self) -> List[V]:
        return self._values

    # --------------------- Modifiers ---------------------
    def insert(self, key: K, value: V) -> bool:
        """
        Inserts value if key not present.
        Returns True if inserted, False if key already existed.
        """
        idx = bisect.bisect_left(self._keys, key)
        if idx < len(self._keys) and self._keys[idx] == key:
            return False
        self._keys.insert(idx, key)
        self._values.insert(idx, value)
        return True

    def insert_or_assign(self, key: K, value: V) -> bool:
        """
        Inserts or updates value.
        Returns True if inserted (new), False if assigned (updated).
        """
        idx = bisect.bisect_left(self._keys, key)
        if idx < len(self._keys) and self._keys[idx] == key:
            self._values[idx] = value
            return False
        self._keys.insert(idx, key)
        self._values.insert(idx, value)
        return True

    def erase(self, key: K) -> int:
        """Removes the element with the given key. Returns 1 if removed, 0 if not found."""
        idx = bisect.bisect_left(self._keys, key)
        if idx < len(self._keys) and self._keys[idx] == key:
            del self._keys[idx]
            del self._values[idx]
            return 1
        return 0

    def swap(self, other: 'FlatMap[K, V]'):
        self._keys, other._keys = other._keys, self._keys
        self._values, other._values = other._values, self._values

    def clear(self):
        self._keys.clear()
        self._values.clear()

    # --------------------- Lookup ---------------------
    def count(self, key: K) -> int:
        idx = bisect.bisect_left(self._keys, key)
        if idx < len(self._keys) and self._keys[idx] == key:
            return 1
        return 0

    def find(self, key: K) -> Iterator[Tuple[K, V]]:
        """Returns iterator to element if found, else None/End (simulated)."""
        idx = bisect.bisect_left(self._keys, key)
        if idx < len(self._keys) and self._keys[idx] == key:
            # Yield single item
            yield (self._keys[idx], self._values[idx])
        # Else empty iterator

    def contains(self, key: K) -> bool:
        return self.count(key) > 0

    def lower_bound(self, key: K) -> int:
        """Returns index of first element >= key."""
        return bisect.bisect_left(self._keys, key)

    def upper_bound(self, key: K) -> int:
        """Returns index of first element > key."""
        return bisect.bisect_right(self._keys, key)
    
    # --------------------- Comparison ---------------------
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FlatMap):
            return NotImplemented
        return self._keys == other._keys and self._values == other._values

    def __repr__(self) -> str:
        # dict-like repr
        kvs = [f"{repr(k)}: {repr(v)}" for k, v in zip(self._keys, self._values)]
        return f"FlatMap({{{', '.join(kvs)}}})"
