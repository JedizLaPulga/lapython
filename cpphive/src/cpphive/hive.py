from __future__ import annotations
from typing import TypeVar, Generic, Iterator, Any, List, Optional
from cppbase import Container

T = TypeVar('T')

class HiveIterator(Generic[T]):
    """Iterator for Hive."""
    __slots__ = ('_hive', '_block_idx', '_slot_idx')

    def __init__(self, hive: Hive[T], block_idx: int, slot_idx: int):
        self._hive = hive
        self._block_idx = block_idx
        self._slot_idx = slot_idx

    def __iter__(self):
        return self

    def __next__(self) -> T:
        # Check if we are at end or invalid
        if not self._is_valid():
            raise StopIteration
        
        # Get current value
        val = self._hive._get_value(self._block_idx, self._slot_idx)
        
        # Advance
        self._advance()
        
        return val

    def _is_valid(self):
        if self._block_idx >= len(self._hive._blocks):
            return False
        return True

    def _advance(self):
        # Find next valid slot
        # This naive skip algorithm is O(skip), but optimized implementation would use skipfield
        # Here we just linear scan.
        # Next slot in current block?
        self._slot_idx += 1
        return self._seek_valid()

    def _seek_valid(self):
        while self._block_idx < len(self._hive._blocks):
            block = self._hive._blocks[self._block_idx]
            while self._slot_idx < len(block):
                if block[self._slot_idx] is not self._hive._TOMBSTONE:
                    return # Found valid
                self._slot_idx += 1
            
            # Move to next block
            self._block_idx += 1
            self._slot_idx = 0
            
    def value(self) -> T:
        """Access value at current position without advancing."""
        return self._hive._get_value(self._block_idx, self._slot_idx)

class Hive(Container, Generic[T]):
    """
    A Python implementation of plf::hive (colony).
    A bucket-array container that allows O(1) insertion and erasure with stable iterators.
    Elements are not moved in memory (in Python: their position/index tuple is stable).
    """
    __slots__ = ('_blocks', '_size', '_free_slots', '_TOMBSTONE')
    
    def __init__(self, source=None):
        self._blocks: List[List[Any]] = []
        self._size = 0
        self._free_slots: List[tuple[int, int]] = [] # Stack of (block_idx, slot_idx)
        self._TOMBSTONE = object() # Unique sentinel for erased slots
        
        if source is not None:
            for x in source:
                self.insert(x)

    def insert(self, value: T):
        """Inserts value and returns an iterator to it."""
        # Reuse free slot
        if self._free_slots:
            b_idx, s_idx = self._free_slots.pop()
            self._blocks[b_idx][s_idx] = value
            self._size += 1
            return HiveIterator(self, b_idx, s_idx)
        
        # Or append
        if not self._blocks:
            self._add_block()
        
        last_block = self._blocks[-1]
        # Check if last block is full (assuming we respect capacities or just handle list growth)
        # Hive usually has geometric block growth.
        # For simplicity in Python, we can just let lists grow or enforce a cap.
        # Strict hive enforces capacity.
        # Let's say block cap: 8, 16, 32...
        current_block_cap = 8 * (2 ** (len(self._blocks) - 1))
        
        if len(last_block) < current_block_cap:
            last_block.append(value)
            b_idx = len(self._blocks) - 1
            s_idx = len(last_block) - 1
            self._size += 1
            return HiveIterator(self, b_idx, s_idx)
        else:
            self._add_block()
            self._blocks[-1].append(value)
            b_idx = len(self._blocks) - 1
            s_idx = 0
            self._size += 1
            return HiveIterator(self, b_idx, s_idx)

    def erase(self, iterator: HiveIterator):
        """Erases element at iterator. Iterator becomes invalid (points to tombstone)."""
        b_idx, s_idx = iterator._block_idx, iterator._slot_idx
        if self._blocks[b_idx][s_idx] is self._TOMBSTONE:
            return # Already erased
        
        self._blocks[b_idx][s_idx] = self._TOMBSTONE
        self._free_slots.append((b_idx, s_idx))
        self._size -= 1

    def clear(self):
        self._blocks.clear()
        self._free_slots.clear()
        self._size = 0

    def empty(self) -> bool:
        return self._size == 0
    
    def size(self) -> int:
        return self._size
    
    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[T]:
        for block in self._blocks:
            for item in block:
                if item is not self._TOMBSTONE:
                    yield item

    # --------------------- Internal ---------------------
    def _add_block(self):
        self._blocks.append([])

    def _get_value(self, b_idx, s_idx):
        if b_idx >= len(self._blocks): raise IndexError("Iterator out of bounds")
        if s_idx >= len(self._blocks[b_idx]): raise IndexError("Iterator out of bounds")
        val = self._blocks[b_idx][s_idx]
        if val is self._TOMBSTONE:
            raise ValueError("Iterator points to erased element")
        return val

    def splice(self, other: Hive):
        """Moves elements from other hive to this one (Not strictly possible efficiently in Python without header manipulation, but we can simulate transfer)"""
        # Strict C++ splice moves nodes. Here we just insert and clear other.
        for x in other:
            self.insert(x)
        other.clear()
        
    def __repr__(self):
        return f"Hive(size={self._size}, items={list(self)})"
