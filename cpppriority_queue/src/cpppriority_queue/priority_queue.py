from __future__ import annotations
from typing import TypeVar, Generic, Any, Callable, List, Iterable
import heapq

T = TypeVar('T')

class PriorityQueue(Generic[T]):
    __slots__ = ('_data', '_comparator')

    def __init__(self, source: Iterable[T] | None = None, key: Callable[[T], Any] | None = None):
        """
        C++ style priority_queue.
        
        Note: C++ std::priority_queue is a MAX heap by default.
        Python's heapq is a MIN heap.
        To strictly mimic C++, we need to invert the comparison logic if we want a max heap,
        or we just document that this is a min-heap (as per Python conventions) OR implementing a max-heap wrapper.
        
        IMPL DECISION: 
        std::priority_queue<T> pops the LARGEST element (Max Heap).
        We will emulate this behavior to be consistent with the C++ specific naming.
        
        Storage:
        We will use a list and heapq functions, but we need to invert keys or handle comparisons manually 
        to achieve Max-Heap behavior for standard types (int, float).
        
        However, fully generic Max-Heap in Python for custom objects is tricky without wrapper classes.
        For simplicity and performance, we will provide a `key` argument (like sorted()) which is standard in Python,
        but default behavior for numbers will be Max Heap.
        """
        self._data: List[Any] = []
        
        # If user provides a key, we use it. 
        # But to make a MAX heap using Python's MIN heap, we typically negate values for numbers.
        # For generic objects, it's harder.
        # Approach: We will store tuples (-priority, item) for numbers? 
        # Or just implement custom sift_up/sift_down implementation?
        # Implementing custom heap logic is safer for "strict" C++ port than fighting heapq's min-logic.
        
        if source is not None:
             for x in source:
                 self.push(x)

    def _sift_up(self, idx: int):
        # Move node up as long as it is GREATER than parent (Max Heap)
        current = idx
        while current > 0:
            parent = (current - 1) // 2
            if self._data[current] > self._data[parent]:
                self._data[current], self._data[parent] = self._data[parent], self._data[current]
                current = parent
            else:
                break

    def _sift_down(self, idx: int):
        # Move node down as long as it is SMALLER than children
        size = len(self._data)
        current = idx
        while True:
            left = 2 * current + 1
            right = 2 * current + 2
            largest = current
            
            if left < size and self._data[left] > self._data[largest]:
                largest = left
            if right < size and self._data[right] > self._data[largest]:
                largest = right
                
            if largest != current:
                self._data[current], self._data[largest] = self._data[largest], self._data[current]
                current = largest
            else:
                break

    def push(self, value: T):
        """Inserts element and sorts underlying container."""
        self._data.append(value)
        self._sift_up(len(self._data) - 1)

    def pop(self):
        """Removes the top element (Max element)."""
        if not self._data:
            raise IndexError("pop from empty priority_queue")
        
        # Swap root with last
        last_idx = len(self._data) - 1
        if last_idx > 0:
            self._data[0], self._data[last_idx] = self._data[last_idx], self._data[0]
            val = self._data.pop() # Remove strict max
            self._sift_down(0)
            return val
        else:
            return self._data.pop()

    def top(self) -> T:
        """Returns the top element (Max element)."""
        if not self._data:
            raise IndexError("top on empty priority_queue")
        return self._data[0]

    def empty(self) -> bool:
        return len(self._data) == 0

    def size(self) -> int:
        return len(self._data)
    
    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self):
        return f"PriorityQueue[{len(self._data)}](top={self.top() if self._data else 'None'})"
