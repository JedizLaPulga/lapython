from typing import MutableSequence, TypeVar, Callable, Optional

T = TypeVar('T')

def _compare(a: T, b: T, comparator: Optional[Callable[[T, T], bool]]) -> bool:
    """
    Returns True if a < b (using comparator if provided).
    """
    if comparator:
        return comparator(a, b)
    return a < b

def push_heap(sequence: MutableSequence[T], comparator: Optional[Callable[[T, T], bool]] = None) -> None:
    """
    Inserts the element at the last position into the max-heap defined by the range [0, len-1).
    The resulting range [0, len) is a valid max-heap.
    
    Equivalent to std::push_heap.
    """
    index = len(sequence) - 1
    if index <= 0:
        return

    # Sift Up
    while index > 0:
        parent_idx = (index - 1) // 2
        # If parent < current, swap (Max Heap)
        if _compare(sequence[parent_idx], sequence[index], comparator):
            sequence[parent_idx], sequence[index] = sequence[index], sequence[parent_idx]
            index = parent_idx
        else:
            break

def _sift_down(sequence: MutableSequence[T], root: int, end: int, comparator: Optional[Callable[[T, T], bool]]) -> None:
    """
    Helper to sift down the element at root in the heap range [0, end).
    """
    largest = root
    
    while True:
        left_child = 2 * largest + 1
        right_child = 2 * largest + 2
        swap_idx = largest

        # Check left child
        if left_child < end:
            # If current < left_child, then left_child is candidate for largest
            if _compare(sequence[swap_idx], sequence[left_child], comparator):
                swap_idx = left_child
        
        # Check right child
        if right_child < end:
            # If current candidate < right_child
            if _compare(sequence[swap_idx], sequence[right_child], comparator):
                swap_idx = right_child

        if swap_idx != largest:
            sequence[largest], sequence[swap_idx] = sequence[swap_idx], sequence[largest]
            largest = swap_idx
        else:
            break

def pop_heap(sequence: MutableSequence[T], comparator: Optional[Callable[[T, T], bool]] = None) -> None:
    """
    Swaps the value in the first position (max) with the value in the last position,
    and makes the subrange [0, len-1) a heap.
    The maximum element is now at the end of the sequence.
    
    Equivalent to std::pop_heap.
    """
    if len(sequence) <= 1:
        return
        
    last_idx = len(sequence) - 1
    # Swap root and last
    sequence[0], sequence[last_idx] = sequence[last_idx], sequence[0]
    
    # Sift down new root within range [0, len-1)
    _sift_down(sequence, 0, last_idx, comparator)

def make_heap(sequence: MutableSequence[T], comparator: Optional[Callable[[T, T], bool]] = None) -> None:
    """
    Constructs a max-heap in the range [0, len).
    
    Equivalent to std::make_heap.
    """
    n = len(sequence)
    if n <= 1:
        return
        
    # Start from last non-leaf node and sift down
    start_idx = (n - 2) // 2
    
    for i in range(start_idx, -1, -1):
        _sift_down(sequence, i, n, comparator)

def sort_heap(sequence: MutableSequence[T], comparator: Optional[Callable[[T, T], bool]] = None) -> None:
    """
    Sorts a heap in range [0, len) into ascending order.
    The sequence is assumed to be a max-heap.
    
    Equivalent to std::sort_heap.
    """
    n = len(sequence)
    if n <= 1:
        return
        
    # Repeatedly pop_heap
    # We manage scope manually to avoid modifying sequence length in loops (pop_heap doesn't resize)
    # pop_heap moves max to end, and restores heap in [0, end-1)
    
    for i in range(n - 1, 0, -1):
        # Swap root (max) with i
        sequence[0], sequence[i] = sequence[i], sequence[0]
        # Restore heap property for [0, i)
        _sift_down(sequence, 0, i, comparator)

def is_heap(sequence: MutableSequence[T], comparator: Optional[Callable[[T, T], bool]] = None) -> bool:
    """
    Returns True if the range is a max-heap.
    
    Equivalent to std::is_heap.
    """
    return is_heap_until(sequence, comparator) == len(sequence)

def is_heap_until(sequence: MutableSequence[T], comparator: Optional[Callable[[T, T], bool]] = None) -> int:
    """
    Returns the index of the first element which violates the max-heap property.
    Returns len(sequence) if the entire range is valid.
    
    Equivalent to std::is_heap_until.
    """
    n = len(sequence)
    parent = 0
    # Loop over parents
    for i in range(1, n):
        parent = (i - 1) // 2
        # If parent < current child, violation
        if _compare(sequence[parent], sequence[i], comparator):
            return i
            
    return n
