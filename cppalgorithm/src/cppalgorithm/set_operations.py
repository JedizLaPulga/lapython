from typing import Iterable, Callable, TypeVar, Any, Union, MutableSequence

T = TypeVar('T')
Destination = Union[MutableSequence[T], Callable[[T], Any]]

def _write(dest: Destination, index: int, value: T) -> int:
    if callable(dest):
        dest(value)
        return index + 1
    else:
        dest[index] = value
        return index + 1

def merge(sorted1: Iterable[T], sorted2: Iterable[T], result: Destination) -> None:
    """
    Merges two sorted ranges into one sorted range.
    Equivalent to std::merge.
    """
    it1 = iter(sorted1)
    it2 = iter(sorted2)
    
    try:
        val1 = next(it1)
        has_val1 = True
    except StopIteration:
        has_val1 = False
        
    try:
        val2 = next(it2)
        has_val2 = True
    except StopIteration:
        has_val2 = False
        
    idx = 0
    
    while has_val1 and has_val2:
        if val2 < val1:
            idx = _write(result, idx, val2)
            try:
                val2 = next(it2)
            except StopIteration:
                has_val2 = False
        else:
            idx = _write(result, idx, val1)
            try:
                val1 = next(it1)
            except StopIteration:
                has_val1 = False
                
    # Exhaust remaining
    while has_val1:
        idx = _write(result, idx, val1)
        try:
            val1 = next(it1)
        except StopIteration:
            break
            
    while has_val2:
        idx = _write(result, idx, val2)
        try:
            val2 = next(it2)
        except StopIteration:
            break

def includes(sorted1: Iterable[T], sorted2: Iterable[T]) -> bool:
    """
    Returns True if sorted2 is a subsequence of sorted1.
    Both must be sorted.
    Equivalent to std::includes.
    """
    it1 = iter(sorted1)
    it2 = iter(sorted2)
    
    try:
        val2 = next(it2)
    except StopIteration:
        return True # Empty set is included in anything
        
    for val1 in it1:
        if val2 < val1:
            return False # val2 not found in sorted1 (passed it)
        elif val1 == val2:
            try:
                val2 = next(it2)
            except StopIteration:
                return True # All of sorted2 found
                
    return False # Exhausted sorted1 before sorted2

def set_union(sorted1: Iterable[T], sorted2: Iterable[T], result: Destination) -> None:
    """
    Constructs a sorted union of two sorted ranges.
    Equivalent to std::set_union.
    """
    it1 = iter(sorted1)
    it2 = iter(sorted2)
    
    try: val1, has1 = next(it1), True
    except StopIteration: has1 = False
    
    try: val2, has2 = next(it2), True
    except StopIteration: has2 = False
    
    idx = 0
    
    while has1 and has2:
        if val1 < val2:
            idx = _write(result, idx, val1)
            try: val1 = next(it1)
            except StopIteration: has1 = False
        elif val2 < val1:
            idx = _write(result, idx, val2)
            try: val2 = next(it2)
            except StopIteration: has2 = False
        else: # Equal
            idx = _write(result, idx, val1)
            try: val1 = next(it1)
            except StopIteration: has1 = False
            try: val2 = next(it2)
            except StopIteration: has2 = False
            
    while has1:
        idx = _write(result, idx, val1)
        try: val1 = next(it1)
        except StopIteration: break
        
    while has2:
        idx = _write(result, idx, val2)
        try: val2 = next(it2)
        except StopIteration: break

def set_intersection(sorted1: Iterable[T], sorted2: Iterable[T], result: Destination) -> None:
    """
    Constructs a sorted intersection of two sorted ranges.
    Equivalent to std::set_intersection.
    """
    it1 = iter(sorted1)
    it2 = iter(sorted2)
    
    try: val1, has1 = next(it1), True
    except StopIteration: has1 = False
    
    try: val2, has2 = next(it2), True
    except StopIteration: has2 = False
    
    idx = 0
    
    while has1 and has2:
        if val1 < val2:
            try: val1 = next(it1)
            except StopIteration: has1 = False
        elif val2 < val1:
            try: val2 = next(it2)
            except StopIteration: has2 = False
        else: # Equal
            idx = _write(result, idx, val1)
            try: val1 = next(it1)
            except StopIteration: has1 = False
            try: val2 = next(it2)
            except StopIteration: has2 = False

def set_difference(sorted1: Iterable[T], sorted2: Iterable[T], result: Destination) -> None:
    """
    Constructs a sorted difference (elements in sorted1 but NOT in sorted2).
    Equivalent to std::set_difference.
    """
    it1 = iter(sorted1)
    it2 = iter(sorted2)
    
    try: val1, has1 = next(it1), True
    except StopIteration: has1 = False
    
    try: val2, has2 = next(it2), True
    except StopIteration: has2 = False
    
    idx = 0
    
    while has1 and has2:
        if val1 < val2:
            idx = _write(result, idx, val1)
            try: val1 = next(it1)
            except StopIteration: has1 = False
        elif val2 < val1:
            try: val2 = next(it2)
            except StopIteration: has2 = False
        else: # Equal
            try: val1 = next(it1)
            except StopIteration: has1 = False
            try: val2 = next(it2)
            except StopIteration: has2 = False
            
    while has1:
        idx = _write(result, idx, val1)
        try: val1 = next(it1)
        except StopIteration: break

def set_symmetric_difference(sorted1: Iterable[T], sorted2: Iterable[T], result: Destination) -> None:
    """
    Constructs a sorted symmetric difference (elements in either but NOT both).
    Equivalent to std::set_symmetric_difference.
    """
    it1 = iter(sorted1)
    it2 = iter(sorted2)
    
    try: val1, has1 = next(it1), True
    except StopIteration: has1 = False
    
    try: val2, has2 = next(it2), True
    except StopIteration: has2 = False
    
    idx = 0
    
    while has1 and has2:
        if val1 < val2:
            idx = _write(result, idx, val1)
            try: val1 = next(it1)
            except StopIteration: has1 = False
        elif val2 < val1:
            idx = _write(result, idx, val2)
            try: val2 = next(it2)
            except StopIteration: has2 = False
        else: # Equal
            try: val1 = next(it1)
            except StopIteration: has1 = False
            try: val2 = next(it2)
            except StopIteration: has2 = False
            
    while has1:
        idx = _write(result, idx, val1)
        try: val1 = next(it1)
        except StopIteration: break
        
    while has2:
        idx = _write(result, idx, val2)
        try: val2 = next(it2)
        except StopIteration: break
