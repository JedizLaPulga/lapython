from typing import Iterable, TypeVar, Optional, Callable, Any, Tuple

T = TypeVar('T')

def min_element(iterable: Iterable[T], key: Optional[Callable[[T], Any]] = None) -> int:
    """
    Returns the index of the smallest element in the range.
    Equivalent to std::min_element (returns iterator).
    """
    min_idx = -1
    min_val = None
    
    for i, val in enumerate(iterable):
        if min_val is None:
            min_val = val
            min_idx = i
        else:
            comp_val = val if key is None else key(val)
            comp_min = min_val if key is None else key(min_val)
            if comp_val < comp_min:
                min_val = val
                min_idx = i
                
    return min_idx

def max_element(iterable: Iterable[T], key: Optional[Callable[[T], Any]] = None) -> int:
    """
    Returns the index of the largest element in the range.
    Equivalent to std::max_element (returns iterator).
    """
    max_idx = -1
    max_val = None
    
    for i, val in enumerate(iterable):
        if max_val is None:
            max_val = val
            max_idx = i
        else:
            comp_val = val if key is None else key(val)
            comp_max = max_val if key is None else key(max_val)
            if comp_val > comp_max:
                max_val = val
                max_idx = i
                
    return max_idx

def minmax_element(iterable: Iterable[T], key: Optional[Callable[[T], Any]] = None) -> Tuple[int, int]:
    """
    Returns pair (min_index, max_index).
    Equivalent to std::minmax_element.
    """
    # Naive single pass can be optimized to 3*N/2 comparisons, 
    # but standard Python generic loop implementation:
    return (min_element(iterable, key), max_element(iterable, key))

def clamp(v: T, lo: T, hi: T) -> T:
    """
    Returns v clamped between lo and hi.
    Equivalent to std::clamp.
    """
    if v < lo: return lo
    if v > hi: return hi
    return v
