from __future__ import annotations
from typing import TypeVar, Generic, Iterable, Iterator, List as PyList, Any
import sys

T = TypeVar('T')

from cppbase import Sequence
class Deque(Sequence, Generic[T]):
    __slots__ = ('_map', '_block_size', '_start_idx', '_size')
    
    # Standard block size for a deque (often 4KB in C++, we use smaller for Python overhead balance)
    # Using 64 items per block seems reasonable for Python objects.
    _BLOCK_SIZE = 64

    def __init__(self, source: Iterable[T] | None = None):
        self._block_size = self._BLOCK_SIZE
        # _map is a list of lists. Each inner list is a "block" of size _BLOCK_SIZE.
        # We start with one empty block.
        self._map: PyList[PyList[Any] | None] = [self._allocate_block()]
        
        # _start_idx is the index in the *first block* where the first element resides.
        self._start_idx = self._BLOCK_SIZE // 2 # Start in the middle to allow some push_front without immediate alloc
        self._size = 0
        
        if source is not None:
            for x in source:
                self.push_back(x)

    def _allocate_block(self) -> PyList[Any]:
        return [None] * self._block_size

    # --------------------- Modifiers ---------------------
    def push_back(self, value: T):
        # Logical position of the new element
        # logical_end is relative to the start of the _map[0] buffer? No.
        # Let's map logical index 0 to (block_0, start_idx).
        
        # Current end position in relative coordinates of the map structure:
        # ABSOLUTE index of the slot after the last element.
        # abs_idx = self._start_idx + self._size
        
        abs_end = self._start_idx + self._size
        block_idx = abs_end // self._block_size
        offset = abs_end % self._block_size
        
        # If block_idx is outside our current map, we need to add blocks
        if block_idx >= len(self._map):
            self._map.append(self._allocate_block())
            
        self._map[block_idx][offset] = value
        self._size += 1

    def push_front(self, value: T):
        if self._start_idx == 0:
            # We need to prepend a new block or shift logic?
            # Creating a new block at the start of the map:
            self._map.insert(0, self._allocate_block())
            # Now the old start_idx (0) becomes start_idx relative to map[1]. 
            # In the NEW map, it is at index: BLOCK_SIZE.
            # So, the new start absolute index should be BLOCK_SIZE - 1.
            self._start_idx = self._block_size
        
        self._start_idx -= 1
        self._map[0][self._start_idx] = value
        self._size += 1

    def pop_back(self) -> T:
        if self._size == 0:
            raise IndexError("pop_back from empty deque")
        
        abs_last = self._start_idx + self._size - 1
        block_idx = abs_last // self._block_size
        offset = abs_last % self._block_size
        
        val = self._map[block_idx][offset]
        self._map[block_idx][offset] = None # Help GC
        self._size -= 1
        
        # Cleanup empty blocks if necessary? 
        # C++ std::deque usually doesn't aggressively free, but we might remove unused blocks 
        # if they are at the ends to save memory, mimicking shrink behaviors optionally.
        # For now, we keep it simple (strict standard behavior doesn't mandate autommatic shrink)
        return val

    def pop_front(self) -> T:
        if self._size == 0:
            raise IndexError("pop_front from empty deque")
        
        val = self._map[0][self._start_idx]
        self._map[0][self._start_idx] = None
        
        self._start_idx += 1
        self._size -= 1
        
        # If we exhausted the first block completely, drop it to keep indices manageable
        if self._start_idx >= self._block_size:
            # Drop the first block
            if len(self._map) > 1: # Don't drop the last remaining block
                self._map.pop(0)
                self._start_idx -= self._block_size
            else:
                # Reset if only 1 block and empty
                if self._size == 0:
                    self._start_idx = self._BLOCK_SIZE // 2

        return val

    def clear(self):
        self._map = [self._allocate_block()]
        self._start_idx = self._BLOCK_SIZE // 2
        self._size = 0

    # --------------------- Access ---------------------
    def __getitem__(self, index: int) -> T:
        if index < 0: index += self._size
        if not (0 <= index < self._size):
            raise IndexError("deque index out of range")
        
        # Calculate real position
        real_idx = self._start_idx + index
        block_idx = real_idx // self._block_size
        offset = real_idx % self._block_size
        
        return self._map[block_idx][offset]  # type: ignore

    def __setitem__(self, index: int, value: T):
        if index < 0: index += self._size
        if not (0 <= index < self._size):
            raise IndexError("deque index out of range")
            
        real_idx = self._start_idx + index
        block_idx = real_idx // self._block_size
        offset = real_idx % self._block_size
        
        self._map[block_idx][offset] = value

    def at(self, index: int) -> T:
        return self[index]

    def front(self) -> T: return self[0]
    def back(self) -> T: return self[self._size - 1]

    def size(self) -> int: return self._size
    def empty(self) -> bool: return self._size == 0
    def __len__(self) -> int: return self._size

    # --------------------- Iterators ---------------------
    def __iter__(self) -> Iterator[T]:
        # Optimization: Iterate block by block to avoid repeated div/mod math
        if self._size == 0:
            return

        # 1. First block partial
        current_abs = self._start_idx
        block_idx = 0
        
        # While strictly inside the deque valid range
        count = 0
        while count < self._size:
            # Get current block
            blk = self._map[block_idx]
            # range in this block
            # start: current_abs (if first block) else 0
            # end: min(block_size, current_abs + remaining items) ??
            # Simpler: just iterate smartly
            
            start_in_blk = current_abs
            end_in_blk = min(self._block_size, start_in_blk + (self._size - count))
            
            for i in range(start_in_blk, end_in_blk):
                yield blk[i] # type: ignore
                count += 1
            
            # Move to next block
            block_idx += 1
            current_abs = 0 # Subsequent blocks start at 0

    def __repr__(self):
        return f"Deque[{self._size}]({list(self)})"
