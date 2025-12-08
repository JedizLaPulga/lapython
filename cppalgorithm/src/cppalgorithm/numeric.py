from typing import Iterable, MutableSequence, TypeVar, Callable, Any, Union

T = TypeVar('T')
U = TypeVar('U')

Destination = Union[MutableSequence[T], Callable[[T], Any]]

def _write(dest: Destination, index: int, value: T) -> int:
    if callable(dest):
        dest(value)
        return index + 1
    else:
        dest[index] = value
        return index + 1

def iota(sequence: MutableSequence[T], value: T) -> None:
    """
    Fills the sequence with sequentially increasing values.
    """
    current = value
    for i in range(len(sequence)):
        sequence[i] = current
        current += 1

def accumulate(iterable: Iterable[T], init: U, op: Callable[[U, T], U] = lambda x, y: x + y) -> U:
    """
    Computes the sum of the given value init and the elements.
    Equivalent to functools.reduce but with optional op.
    """
    result = init
    for item in iterable:
        result = op(result, item)
    return result

def inner_product(seq1: Iterable[T], seq2: Iterable[T], init: U) -> U:
    """
    Computes the inner product (dot product) of two ranges.
    """
    result = init
    for a, b in zip(seq1, seq2):
        result = result + (a * b)
    return result

def partial_sum(source: Iterable[T], result: Destination) -> None:
    """
    Calculates the prefix sum.
    e.g. [1, 2, 3] -> [1, 3, 6]
    """
    current_sum = None
    idx = 0
    for item in source:
        if current_sum is None:
            current_sum = item
        else:
            current_sum = current_sum + item
        idx = _write(result, idx, current_sum)

def adjacent_difference(source: Iterable[T], result: Destination) -> None:
    """
    Calculates differences between adjacent elements.
    e.g. [1, 2, 5] -> [1, 1, 3] (first element is copy of source)
    """
    prev = None
    idx = 0
    for item in source:
        if prev is None:
            val = item
        else:
            val = item - prev
        idx = _write(result, idx, val)
        prev = item
