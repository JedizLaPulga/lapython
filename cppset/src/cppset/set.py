from __future__ import annotations
from typing import TypeVar, Generic, Iterator, Any, Union

T = TypeVar('T')

class _Node(Generic[T]):
    __slots__ = ('key', 'left', 'right', 'parent')
    
    def __init__(self, key: T, parent: _Node[T] | None = None):
        self.key = key
        self.left: _Node[T] | None = None
        self.right: _Node[T] | None = None
        self.parent = parent

class Set(Generic[T]):
    __slots__ = ('_root', '_size')
    
    # std::set implementation (Ordered Unique Keys)
    # Uses BST (O(log N) average).
    
    def __init__(self, source=None):
        self._root: _Node[T] | None = None
        self._size = 0
        
        if source is not None:
            for x in source:
                self.insert(x)

    # --------------------- Modifiers ---------------------
    def insert(self, key: T):
        if not self._root:
            self._root = _Node(key)
            self._size += 1
            return

        curr = self._root
        while True:
            if key < curr.key:
                if curr.left:
                    curr = curr.left
                else:
                    curr.left = _Node(key, curr)
                    self._size += 1
                    break
            elif key > curr.key:
                if curr.right:
                    curr = curr.right
                else:
                    curr.right = _Node(key, curr)
                    self._size += 1
                    break
            else:
                # Duplicate, do nothing (std::set stores unique keys)
                break

    def erase(self, key: T):
        node = self._find_node(key)
        if not node:
            return
        
        self._delete_node(node)
        self._size -= 1

    def clear(self):
        self._root = None
        self._size = 0

    # --------------------- Access ---------------------
    def find(self, key: T) -> T | None:
        """Returns key if found, else None (iterator end)."""
        node = self._find_node(key)
        return node.key if node else None

    def count(self, key: T) -> int:
        return 1 if self._find_node(key) else 0

    def contains(self, key: T) -> bool:
        return self._find_node(key) is not None

    def empty(self) -> bool: return self._size == 0
    def size(self) -> int: return self._size
    def __len__(self) -> int: return self._size

    # --------------------- Traversal (Sorted) ---------------------
    def __iter__(self) -> Iterator[T]:
        """In-order traversal yielding sorted keys."""
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
                yield curr.key
                curr = curr.right
            else:
                break
    
    # --------------------- Range ---------------------
    def lower_bound(self, key: T) -> T | None:
        """Returns first element >= key."""
        curr = self._root
        result = None
        while curr:
            if curr.key >= key:
                result = curr.key
                curr = curr.left
            else:
                curr = curr.right
        return result

    def upper_bound(self, key: T) -> T | None:
        """Returns first element > key."""
        curr = self._root
        result = None
        while curr:
            if curr.key > key:
                result = curr.key
                curr = curr.left
            else:
                curr = curr.right
        return result

    # --------------------- Internal ---------------------
    def _find_node(self, key: T) -> _Node[T] | None:
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
        return f"Set({{{', '.join(repr(x) for x in self)}}})"
