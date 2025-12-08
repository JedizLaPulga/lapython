from typing import Iterable, Callable, TypeVar, Any, MutableSequence, Union

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
