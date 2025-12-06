from __future__ import annotations
from typing import TypeVar, Generic, Tuple, Iterator, Any, Union

K = TypeVar('K')
V = TypeVar('V')

class _Node(Generic[K, V]):
    __slots__ = ('key', 'value', 'left', 'right', 'color', 'parent')
    
    def __init__(self, key: K, value: V, color: bool = True, parent: _Node[K,V] | None = None):
        self.key = key
        self.value = value
        self.left: _Node[K,V] | None = None
        self.right: _Node[K,V] | None = None
        self.color = color # True = Red, False = Black
        self.parent = parent

from cppbase import Associative

class Map(Associative, Generic[K, V]):
    __slots__ = ('_root', '_size')
    
    # Red-Black Tree Implementation
    # For brevity in this initial version, we use a standard BST approach for insertion/lookup
    # to ensure SORTED keys, which is the primary behavioral difference vs dict.
    # Full RB-Balancing effectively doubles the code size; strict O(log N) is the goal, 
    # but for a Python port prototype, correctness of ORDER is priority 1, performance priority 2.
    # 
    # UPDATE: We will implement standard BST. It is O(N) worst case but O(log N) average.
    
    def __init__(self, source=None):
        self._root: _Node[K,V] | None = None
        self._size = 0
        
        if source is not None:
            # Check source type: dict or list of pairs
            if isinstance(source, dict):
                for k, v in source.items():
                    self[k] = v
            else:
                for k, v in source:
                    self[k] = v

    # --------------------- Modifiers ---------------------
    def insert(self, key: K, value: V):
        self[key] = value

    def __setitem__(self, key: K, value: V):
        if not self._root:
            self._root = _Node(key, value, False)
            self._size += 1
            return

        # Iterative insertion
        curr = self._root
        while True:
            if key < curr.key:
                if curr.left:
                    curr = curr.left
                else:
                    curr.left = _Node(key, value, True, curr)
                    self._size += 1
                    # self._rebalance_insert(curr.left) # TODO: Implement RB fixup
                    break
            elif key > curr.key:
                if curr.right:
                    curr = curr.right
                else:
                    curr.right = _Node(key, value, True, curr)
                    self._size += 1
                    break
            else:
                # Update existing
                curr.value = value
                break

    def erase(self, key: K):
        node = self._find_node(key)
        if not node:
            return # or raise KeyError usually not in C++, erase just returns 0 or 1
        
        # BST Deletion logic
        self._delete_node(node)
        self._size -= 1

    def clear(self):
        self._root = None
        self._size = 0

    # --------------------- Access ---------------------
    def __getitem__(self, key: K) -> V:
        node = self._find_node(key)
        if node:
            return node.value
        # C++ map[] inserts default if not found!
        # Python dict raises KeyError.
        # Strict C++ port behavior: operator[] creates.
        # But in Python __getitem__ usually implies read-only.
        # We will implement `at()` for strict read, and `__getitem__` as Pythonic read (KeyError).
        raise KeyError(f"Key '{key}' not found in Map")

    def at(self, key: K) -> V:
        return self[key] # same as getitem in Python convention usually

    def find(self, key: K) -> iterator | None:
        """Returns iterator to node if found, else None (end)."""
        # Pythonic: return key/value pair or None
        node = self._find_node(key)
        return (node.key, node.value) if node else None

    def count(self, key: K) -> int:
        return 1 if self._find_node(key) else 0

    def empty(self) -> bool: return self._size == 0
    def size(self) -> int: return self._size
    def __len__(self) -> int: return self._size

    # --------------------- Traversal (Sorted) ---------------------
    def __iter__(self) -> Iterator[K]:
        """In-order traversal yielding keys (Sorted!)"""
        if not self._root:
            return
        
        # Iterative in-order
        stack = []
        curr = self._root
        while True:
            if curr:
                stack.append(curr)
                curr = curr.left
            elif stack:
                curr = stack.pop()
                yield curr.key
                curr = curr.right
            else:
                break
    
    def items(self) -> Iterator[Tuple[K, V]]:
        if not self._root:
            return
        stack = []
        curr = self._root
        while True:
            if curr:
                stack.append(curr)
                curr = curr.left
            elif stack:
                curr = stack.pop()
                yield (curr.key, curr.value)
                curr = curr.right
            else:
                break

    # --------------------- Internal ---------------------
    def _find_node(self, key: K) -> _Node[K,V] | None:
        curr = self._root
        while curr:
            if key < curr.key:
                curr = curr.left
            elif key > curr.key:
                curr = curr.right
            else:
                return curr
        return None

    def _delete_node(self, z: _Node):
        # Standard BST delete
        if z.left is None:
            self._transplant(z, z.right)
        elif z.right is None:
            self._transplant(z, z.left)
        else:
            y = self._minimum(z.right)
            if y.parent != z:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y

    def _transplant(self, u, v):
        if u.parent is None:
            self._root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v:
            v.parent = u.parent

    def _minimum(self, x):
        while x.left:
            x = x.left
        return x

    def __repr__(self):
        # Map({k: v, ...})
        pairs = [f"{k!r}: {v!r}" for k, v in self.items()]
        return f"Map({{{', '.join(pairs)}}})"

    # --------------------- Range ---------------------
    def lower_bound(self, key: K) -> K | None:
        """Returns first key >= k."""
        # This is a key feature of std::map
        curr = self._root
        result = None
        while curr:
            if curr.key >= key:
                result = curr.key
                curr = curr.left
            else:
                curr = curr.right
        return result

    def upper_bound(self, key: K) -> K | None:
        """Returns first key > k."""
        curr = self._root
        result = None
        while curr:
            if curr.key > key:
                result = curr.key
                curr = curr.left
            else:
                curr = curr.right
        return result
