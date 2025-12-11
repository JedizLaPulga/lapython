from typing import Iterable, Callable, TypeVar, Any, MutableSequence, Union, Optional
import random

T = TypeVar('T')
U = TypeVar('U')

# Destination can be a MutableSequence (assumes space exists) or a Callable (like list.append)
Destination = Union[MutableSequence[T], Callable[[T], Any]]

def _write(dest: Destination, index: int, value: T) -> int:
    """Helper to write to destination. Returns next index."""
    if callable(dest):
        dest(value)
        return index + 1
    else:
        # It's a MutableSequence
        dest[index] = value
        return index + 1

def copy(source: Iterable[T], result: Destination) -> None:
    """
    Copies elements from source to result.
    If result is a Sequence, it MUST have enough space (like std::copy).
    If result is a Callable (e.g. list.append), it appends (like std::back_inserter).
    """
    idx = 0
    for item in source:
        idx = _write(result, idx, item)

def copy_if(source: Iterable[T], result: Destination, predicate: Callable[[T], bool]) -> None:
    """Copies elements satisfying predicate."""
    idx = 0
    for item in source:
        if predicate(item):
            idx = _write(result, idx, item)

def copy_n(source: Iterable[T], n: int, result: Destination) -> None:
    """Copies first n elements."""
    idx = 0
    count = 0
    for item in source:
        if count >= n:
            break
        idx = _write(result, idx, item)
        count += 1

def fill(sequence: MutableSequence[T], value: T) -> None:
    """Assigns value to every element in the sequence."""
    for i in range(len(sequence)):
        sequence[i] = value

def fill_n(sequence: MutableSequence[T], n: int, value: T) -> None:
    """Assigns value to first n elements."""
    for i in range(n):
        sequence[i] = value

def generate(sequence: MutableSequence[T], generator: Callable[[], T]) -> None:
    """Assigns the result of generator() to each element."""
    for i in range(len(sequence)):
        sequence[i] = generator()

def transform(source: Iterable[T], result: Destination, unary_op: Callable[[T], U]) -> None:
    """
    Applies unary_op to each element of source and writes to result.
    Equivalent to std::transform (unary).
    """
    idx = 0
    for item in source:
        idx = _write(result, idx, unary_op(item))

def replace(sequence: MutableSequence[T], old_value: T, new_value: T) -> None:
    """Replaces all occurrences of old_value with new_value in place."""
    for i in range(len(sequence)):
        if sequence[i] == old_value:
            sequence[i] = new_value

def replace_if(sequence: MutableSequence[T], predicate: Callable[[T], bool], new_value: T) -> None:
    """Replaces elements satisfying predicate with new_value in place."""
    for i in range(len(sequence)):
        if predicate(sequence[i]):
            sequence[i] = new_value

def remove(sequence: MutableSequence[T], value: T) -> int:
    """
    Remove elements equal to value.
    Returns the new logical end of the sequence.
    Does NOT resize the sequence (equivalent to std::remove).
    """
    first = 0
    for i in range(len(sequence)):
        if sequence[i] != value:
            if first != i:
                sequence[first] = sequence[i]
            first += 1
    return first

def remove_if(sequence: MutableSequence[T], predicate: Callable[[T], bool]) -> int:
    """
    Remove elements satisfying predicate.
    Returns the new logical end of the sequence.
    Does NOT resize the sequence (equivalent to std::remove_if).
    """
    first = 0
    for i in range(len(sequence)):
        if not predicate(sequence[i]):
            if first != i:
                sequence[first] = sequence[i]
            first += 1
    return first

def unique(sequence: MutableSequence[T], binary_predicate: Optional[Callable[[T, T], bool]] = None) -> int:
    """
    Removes consecutive duplicate elements.
    Returns the new logical end of the sequence.
    Does NOT resize the sequence (equivalent to std::unique).
    """
    if not sequence:
        return 0
    
    first = 0
    for i in range(1, len(sequence)):
        is_equal = False
        if binary_predicate:
            is_equal = binary_predicate(sequence[first], sequence[i])
        else:
            is_equal = (sequence[first] == sequence[i])
            
        if not is_equal:
            first += 1
            sequence[first] = sequence[i]
            
    return first + 1

def reverse(sequence: MutableSequence[T]) -> None:
    """Reverses the sequence in-place."""
    sequence.reverse()

def rotate(sequence: MutableSequence[T], middle: int) -> int:
    """
    Rotates the sequence so that the element at middle becomes the first element.
    Returns the new index of the element that was previously at the beginning (which corresponds to len - middle if rotated left).
    Note: std::rotate returns iterator to the element originally at first, which is now at (last - (middle - first)).
    Here we implement efficiently using slice assignment if possible, or reversal algorithm.
    """
    if not sequence:
        return 0
    n = len(sequence)
    middle %= n # Handle wrapping if needed, though STL usually expects valid iterator
    
    # Pythonic rotation using slicing for lists
    if isinstance(sequence, list):
        sequence[:] = sequence[middle:] + sequence[:middle]
        return n - middle
    else:
        # Generic reversal algorithm
        # reverse(first, middle)
        # reverse(middle, last)
        # reverse(first, last)
        # This is hard to do with just slicing on generic MutableSequence
        # So we do manual swaps
        # But for Python, simpler to just assume list-like or implement generic reversal helper?
        # We'll rely on our reverse implementation if it supported slices, but it just calls .reverse().
        # Let's do a naive rotation for non-lists:
        import collections
        d = collections.deque(sequence)
        d.rotate(-middle)
        for i, item in enumerate(d):
            sequence[i] = item
        return n - middle

def shuffle(sequence: MutableSequence[T], random_engine: Optional[random.Random] = None) -> None:
    """Shuffles the sequence in-place using Knuth shuffle."""
    if random_engine:
        random_engine.shuffle(sequence)
    else:
        random.shuffle(sequence)

def partition(sequence: MutableSequence[T], predicate: Callable[[T], bool]) -> int:
    """
    Reorders elements such that elements satisfying predicate precede those that don't.
    Returns the index of the first element NOT satisfying the predicate.
    """
    first = 0
    last = len(sequence) - 1
    
    while True:
        while first <= last and predicate(sequence[first]):
            first += 1
        while first <= last and not predicate(sequence[last]):
            last -= 1
        if first >= last:
            return first
        # swap
        sequence[first], sequence[last] = sequence[last], sequence[first]
        first += 1
        last -= 1

def stable_partition(sequence: MutableSequence[T], predicate: Callable[[T], bool]) -> int:
    """
    Same as partition but preserves relative order of elements in each group.
    Returns the index of the first element NOT satisfying the predicate.
    """
    # Naive O(N) space implementation
    true_part = []
    false_part = []
    for item in sequence:
        if predicate(item):
            true_part.append(item)
        else:
            false_part.append(item)
            
    # Write back
    idx = 0
    for item in true_part:
        sequence[idx] = item
        idx += 1
    split_point = idx
    for item in false_part:
        sequence[idx] = item
        idx += 1
        
    return split_point
