from typing import Iterable, Callable, TypeVar, Any, Optional

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
