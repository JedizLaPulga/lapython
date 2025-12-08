from typing import MutableSequence, Sequence, TypeVar, Callable, Optional, Any
import bisect

T = TypeVar('T')

def sort(sequence: MutableSequence[T], key: Optional[Callable[[T], Any]] = None, reverse: bool = False) -> None:
    """
    Sorts the elements in the range. 
    Uses Python's Timsort (which is stable, so effectively stable_sort).
    """
    # If it has a .sort() method (list), use it for speed.
    if hasattr(sequence, 'sort'):
        sequence.sort(key=key, reverse=reverse)
    else:
        # Fallback for generic MutableSequence: sort and replace
        sorted_data = sorted(sequence, key=key, reverse=reverse)
        for i, val in enumerate(sorted_data):
            sequence[i] = val

def stable_sort(sequence: MutableSequence[T], key: Optional[Callable[[T], Any]] = None, reverse: bool = False) -> None:
    """
    Sorts preserving the order of equivalents.
    In Python, 'sort' is already stable.
    """
    sort(sequence, key, reverse)

def is_sorted(sequence: Sequence[T], key: Optional[Callable[[T], Any]] = None) -> bool:
    """Checks if the sequence is sorted."""
    if len(sequence) < 2:
        return True
    
    iterator = iter(sequence)
    prev = next(iterator)
    if key:
        prev_k = key(prev)
        for item in iterator:
            curr_k = key(item)
            if curr_k < prev_k:
                return False
            prev_k = curr_k
    else:
        for item in iterator:
            if item < prev:
                return False
            prev = item
    return True

def lower_bound(sequence: Sequence[T], value: T, key: Optional[Callable[[T], Any]] = None) -> int:
    """
    Returns index of first element that does not compare less than value (>=).
    Requirement: Sequence must be sorted!
    """
    return bisect.bisect_left(sequence, value, key=key) if key else bisect.bisect_left(sequence, value)

def upper_bound(sequence: Sequence[T], value: T, key: Optional[Callable[[T], Any]] = None) -> int:
    """
    Returns index of first element that compares greater than value (>).
    Requirement: Sequence must be sorted!
    """
    return bisect.bisect_right(sequence, value, key=key) if key else bisect.bisect_right(sequence, value)

def binary_search(sequence: Sequence[T], value: T, key: Optional[Callable[[T], Any]] = None) -> bool:
    """
    Returns True if value is found in sorted sequence.
    """
    idx = lower_bound(sequence, value, key)
    if idx < len(sequence) and (sequence[idx] == value):
        return True
    return False
