from __future__ import annotations
from typing import TypeVar, Generic, Tuple, Iterator, Any, List
from cppbase import Associative

K = TypeVar('K')
V = TypeVar('V')

class _Node(Generic[K, V]):
    __slots__ = ('key', 'value', 'left', 'right', 'parent')
    
    def __init__(self, key: K, value: V, parent: _Node[K,V] | None = None):
        self.key = key
        self.value = value
        self.left: _Node[K,V] | None = None
        self.right: _Node[K,V] | None = None
        self.parent = parent

class MultiMap(Associative, Generic[K, V]):
    """
    Sorted associative container that contains key-value pairs with NOT unique keys.
    Keys are sorted. Multiple elements with the same key are allowed.
    """
    __slots__ = ('_root', '_size')
    
    def __init__(self, source=None):
        self._root: _Node[K,V] | None = None
        self._size = 0
        
        if source is not None:
            # Source should be iterable of (k, v)
            if isinstance(source, dict):
                for k, v in source.items():
                    self.insert(k, v)
            else:
                for k, v in source:
                    self.insert(k, v)

    # --------------------- Modifiers ---------------------
    def insert(self, key: K, value: V):
        """Inserts element, even if key exists."""
        if not self._root:
            self._root = _Node(key, value)
            self._size += 1
            return

        curr = self._root
        while True:
            if key < curr.key:
                if curr.left:
                    curr = curr.left
                else:
                    curr.left = _Node(key, value, curr)
                    self._size += 1
                    break
            # Unlike Map, if key >= curr.key, we go right for duplicates too (or left, convention choice)
            # Typically for stability or just consistency, duplicates go to one side.
            # STL usually implies duplicates are adjacent in traversal.
            # If we put duplicates to the RIGHT:
            else: 
                if curr.right:
                    curr = curr.right
                else:
                    curr.right = _Node(key, value, curr)
                    self._size += 1
                    break
    
    def erase(self, key: K) -> int:
        """Removes ALL elements with key. Returns count removed."""
        count = 0
        while True:
            node = self._find_first_node(key)
            if not node:
                break
            
            # Since we might have multiple, we need to be careful.
            # _find_first_node finds *some* node. 
            # If we just delete one, we need to loop.
            # Optimization: could find range and delete.
            # For this MVP, iterative deletion of found nodes is acceptable if O(N) worst case.
            # BUT: _find_first_node might find the same one if duplicates are spread?
            # Actually, standard BST find might hit *any* duplicate.
            # To correctly remove all, we can iterate while find(key) returns something.
            
            self._delete_node(node)
            self._size -= 1
            count += 1
        return count

    def clear(self):
        self._root = None
        self._size = 0

    # --------------------- Access ---------------------
    def find(self, key: K) -> Iterator[Tuple[K,V]] | None:
        """Returns iterator to first finding of key, or None."""
        node = self._find_first_node(key)
        # In C++, find returns iterator to *one* of the elements.
        # Pythonic: we'll return the (key, value)
        return (node.key, node.value) if node else None

    def count(self, key: K) -> int:
        c = 0
        # Iterate and count matches
        # This is O(N) worst case in standard BST without metadata.
        # But we can optimize by finding one, then checking neighbors if we had a linear iterator.
        # Traversal approach:
        stack = []
        curr = self._root
        while True:
            if curr:
                stack.append(curr)
                curr = curr.left
            elif stack:
                curr = stack.pop()
                if curr.key == key:
                    c += 1
                elif curr.key > key:
                    # Sorted, so we can stop early
                    break
                curr = curr.right
            else:
                break
        return c

    def equal_range(self, key: K) -> Iterator[Tuple[K,V]]:
        """Returns iterator yielding all pairs satisfying key."""
        stack = []
        curr = self._root
        while True:
            if curr:
                stack.append(curr)
                curr = curr.left
            elif stack:
                curr = stack.pop()
                if curr.key == key:
                    yield (curr.key, curr.value)
                elif curr.key > key:
                    break
                curr = curr.right
            else:
                break

    def empty(self) -> bool: return self._size == 0
    def size(self) -> int: return self._size
    def __len__(self) -> int: return self._size

    # --------------------- Traversal ---------------------
    def __iter__(self) -> Iterator[K]:
        """In-order traversal yielding keys."""
        if not self._root: return
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
        if not self._root: return
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
    def _find_first_node(self, key: K) -> _Node[K,V] | None:
        curr = self._root
        found = None
        while curr:
            if key < curr.key:
                curr = curr.left
            elif key > curr.key:
                curr = curr.right
            else:
                # Found one, but for erase/count we might want specific traversals.
                # Just return strict match.
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
        pairs = [f"{k!r}: {v!r}" for k, v in self.items()]
        return f"MultiMap({{{', '.join(pairs)}}})"
