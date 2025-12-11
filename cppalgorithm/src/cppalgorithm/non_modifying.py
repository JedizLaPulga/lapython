from typing import Iterable, Callable, TypeVar, Any, Optional, Tuple, Sequence
import collections

T = TypeVar('T')

def for_each(iterable: Iterable[T], func: Callable[[T], Any]) -> None:
    """
    Applies the given function to each element of the iterable.
    Equivalent to: std::for_each
    """
    for item in iterable:
        func(item)

def find(iterable: Iterable[T], value: T) -> int:
    """
    Returns the index of the first element equal to value.
    Returns -1 if not found.
    Equivalent to: std::find (returning index instead of iterator)
    """
    for i, item in enumerate(iterable):
        if item == value:
            return i
    return -1

def find_if(iterable: Iterable[T], predicate: Callable[[T], bool]) -> int:
    """
    Returns the index of the first element satisfying the predicate.
    Returns -1 if not found.
    Equivalent to: std::find_if
    """
    for i, item in enumerate(iterable):
        if predicate(item):
            return i
    return -1

def find_if_not(iterable: Iterable[T], predicate: Callable[[T], bool]) -> int:
    """
    Returns the index of the first element NOT satisfying the predicate.
    Returns -1 if not found.
    Equivalent to: std::find_if_not
    """
    for i, item in enumerate(iterable):
        if not predicate(item):
            return i
    return -1

def count(iterable: Iterable[T], value: T) -> int:
    """
    Returns the number of elements equal to value.
    Equivalent to: std::count
    """
    c = 0
    for item in iterable:
        if item == value:
            c += 1
    return c

def count_if(iterable: Iterable[T], predicate: Callable[[T], bool]) -> int:
    """
    Returns the number of elements satisfying the predicate.
    Equivalent to: std::count_if
    """
    c = 0
    for item in iterable:
        if predicate(item):
            c += 1
    return c

def all_of(iterable: Iterable[T], predicate: Callable[[T], bool]) -> bool:
    """Returns True if predicate is true for all elements."""
    for item in iterable:
        if not predicate(item):
            return False
    return True

def any_of(iterable: Iterable[T], predicate: Callable[[T], bool]) -> bool:
    """Returns True if predicate is true for at least one element."""
    for item in iterable:
        if predicate(item):
            return True
    return False

def none_of(iterable: Iterable[T], predicate: Callable[[T], bool]) -> bool:
    """Returns True if predicate is true for no elements."""
    for item in iterable:
        if predicate(item):
            return False
    return True

def mismatch(iterable1: Iterable[T], iterable2: Iterable[T], 
             predicate: Optional[Callable[[T, T], bool]] = None) -> Tuple[int, int]:
    """
    Returns the first index where two iterables differ.
    Returns (-1, -1) if they are equal (up to the length of the shorter one, 
    or if both end together). 
    Wait, C++ returns pair of iterators to the first mismatch.
    If no mismatch found (one sequence exhausted), returns (end, corresponding).
    
    Here: returns (index, index) of the first mismatch.
    If one is shorter and matches prefix of other, returns (len_shorter, len_shorter).
    If both end same time and match, returns (len, len).
    """
    iter1 = iter(iterable1)
    iter2 = iter(iterable2)
    idx = 0
    while True:
        try:
            val1 = next(iter1)
        except StopIteration:
            val1 = None
            
        try:
            val2 = next(iter2)
        except StopIteration:
            val2 = None
            
        if val1 is None and val2 is None:
            # Both ended
            return (idx, idx)
        
        if val1 is None or val2 is None:
            # One ended => mismatch at idx
            return (idx, idx)
            
        is_same = False
        if predicate:
            is_same = predicate(val1, val2)
        else:
            is_same = (val1 == val2)
            
        if not is_same:
            return (idx, idx)
            
        idx += 1

def equal(iterable1: Iterable[T], iterable2: Iterable[T], 
          predicate: Optional[Callable[[T, T], bool]] = None) -> bool:
    """
    Returns True if ranges are equal.
    Considers lengths.
    """
    iter1 = iter(iterable1)
    iter2 = iter(iterable2)
    
    while True:
        try:
            val1 = next(iter1)
        except StopIteration:
            val1 = None
            
        try:
            val2 = next(iter2)
        except StopIteration:
            val2 = None
            
        if val1 is None and val2 is None:
            return True
        if val1 is None or val2 is None:
            return False
            
        is_same = False
        if predicate:
            is_same = predicate(val1, val2)
        else:
            is_same = (val1 == val2)
            
        if not is_same:
            return False

def is_permutation(iterable1: Iterable[T], iterable2: Iterable[T], 
                   predicate: Optional[Callable[[T, T], bool]] = None) -> bool:
    """
    Returns True if iterable1 is a permutation of iterable2.
    """
    # If predicate is None, use Counter for O(N)
    if predicate is None:
        return collections.Counter(iterable1) == collections.Counter(iterable2)
    
    # If predicate is custom, O(N^2)
    # Convert to lists
    list1 = list(iterable1)
    list2 = list(iterable2)
    
    if len(list1) != len(list2):
        return False
        
    # For each element in list1, try to find a match in list2 and remove it (or mark used)
    # To handle duplicates correctly with custom predicate, we need to match counts.
    # This is expensive: O(N^2)
    matched = [False] * len(list2)
    for item1 in list1:
        found = False
        for i, item2 in enumerate(list2):
            if not matched[i]:
                if predicate(item1, item2):
                    matched[i] = True
                    found = True
                    break
        if not found:
            return False
    return True

def lexicographical_compare(iterable1: Iterable[T], iterable2: Iterable[T], 
                            comparator: Optional[Callable[[T, T], bool]] = None) -> bool:
    """
    Returns True if iterable1 is lexicographically less than iterable2.
    """
    iter1 = iter(iterable1)
    iter2 = iter(iterable2)
    
    while True:
        try:
            val1 = next(iter1)
        except StopIteration:
            val1 = None
            
        try:
            val2 = next(iter2)
        except StopIteration:
            val2 = None
            
        if val2 is None:
            # iter2 ended (or both ended)
            # if iter2 ended, iter1 cannot be strictly less unless iter1 also ended (then equal)
            # if both ended, equal -> False (strictly less check usually)
            return False
        if val1 is None:
            # iter1 ended, iter2 has value -> iter1 < iter2
            return True
            
        # Compare values
        if comparator:
            if comparator(val1, val2): # val1 < val2
                return True
            if comparator(val2, val1): # val2 < val1 => val1 > val2
                return False
            # equal, continue
        else:
            if val1 < val2:
                return True
            if val2 < val1:
                return False
            # equal continue

def search(sequence: Sequence[T], subsequence: Sequence[T], 
           predicate: Optional[Callable[[T, T], bool]] = None) -> int:
    """
    Searches for the first occurrence of subsequence in sequence.
    Returns the starting index of the match, or -1 if not found.
    Equivalent to std::search.
    """
    n = len(sequence)
    m = len(subsequence)
    
    if m == 0:
        return 0
    if m > n:
        return -1
        
    for i in range(n - m + 1):
        match = True
        for j in range(m):
            if predicate:
                if not predicate(sequence[i + j], subsequence[j]):
                    match = False
                    break
            else:
                if sequence[i + j] != subsequence[j]:
                    match = False
                    break
        if match:
            return i
            
    return -1

def find_end(sequence: Sequence[T], subsequence: Sequence[T],
             predicate: Optional[Callable[[T, T], bool]] = None) -> int:
    """
    Searches for the LAST occurrence of subsequence in sequence.
    Returns the starting index of the match, or -1 if not found.
    Equivalent to std::find_end.
    """
    n = len(sequence)
    m = len(subsequence)
    
    if m == 0:
        return n # C++ says last iterator, in indices maybe length? or 0? 
                 # std::find_end with empty sub returns last.
    if m > n:
        return -1
        
    # Search backwards
    for i in range(n - m, -1, -1):
        match = True
        for j in range(m):
            if predicate:
                if not predicate(sequence[i + j], subsequence[j]):
                    match = False
                    break
            else:
                if sequence[i + j] != subsequence[j]:
                    match = False
                    break
        if match:
            return i
            
    return -1

def find_first_of(sequence: Sequence[T], search_elements: Sequence[T],
                  predicate: Optional[Callable[[T, T], bool]] = None) -> int:
    """
    Searches sequence for any of the elements in search_elements.
    Returns the index of the first match, or -1 if not found.
    Equivalent to std::find_first_of.
    """
    # If no predicate, use set for O(1) lookup if possible, but only if elements are hashable
    # But to stay generic and support unhashable types, we usually do O(N*M).
    # IF predicate is provided, we MUST do O(N*M).
    
    for i, val in enumerate(sequence):
        for s_val in search_elements:
            if predicate:
                if predicate(val, s_val):
                    return i
            else:
                if val == s_val:
                    return i
    return -1

def adjacent_find(sequence: Sequence[T], predicate: Optional[Callable[[T, T], bool]] = None) -> int:
    """
    Searches for two consecutive identical elements.
    Returns the index of the first element of the pair, or -1.
    Equivalent to std::adjacent_find.
    """
    n = len(sequence)
    if n < 2:
        return -1
        
    iterator = iter(sequence)
    prev = next(iterator)
    idx = 0
    
    for curr in iterator:
        if predicate:
            if predicate(prev, curr):
                return idx
        else:
            if prev == curr:
                return idx
        prev = curr
        idx += 1
        
    return -1

def search_n(sequence: Sequence[T], count: int, value: T, 
             predicate: Optional[Callable[[T, T], bool]] = None) -> int:
    """
    Searches for a sequence of 'count' consecutive elements equal to value.
    Returns the starting index, or -1.
    Equivalent to std::search_n.
    """
    if count <= 0:
        return 0
    
    n = len(sequence)
    if n < count:
        return -1
        
    # Naive O(N*count) is safe but can be optimized to O(N) easily.
    # We just need to count consecutive matches.
    current_count = 0
    start_idx = -1
    
    for i, item in enumerate(sequence):
        match = False
        if predicate:
            match = predicate(item, value)
        else:
            match = (item == value)
            
        if match:
            if current_count == 0:
                start_idx = i
            current_count += 1
            if current_count == count:
                return start_idx
        else:
            current_count = 0
            start_idx = -1
            
    return -1