from typing import TypeVar, Any

T = TypeVar('T')
U = TypeVar('U')

def swap(a: list, i: int, j: int) -> None:
    """
    Swaps the elements at indices i and j in the sequence a.
    Python doesn't support swapping non-reference local variables directly via a function,
    so we simulate std::swap for collections.
    """
    a[i], a[j] = a[j], a[i]

def exchange(obj: list, index: int, new_val: T) -> T:
    """
    Replaces the value of obj[index] with new_val and returns the old value.
    """
    old_val = obj[index]
    obj[index] = new_val
    return old_val

def as_const(obj: T) -> T:
    """
    Casts to const. In Python, this is mostly a semantic marker.
    """
    return obj

def cmp_equal(t: int, u: int) -> bool:
    return t == u

def cmp_not_equal(t: int, u: int) -> bool:
    return t != u

def cmp_less(t: int, u: int) -> bool:
    return t < u

def cmp_greater(t: int, u: int) -> bool:
    return t > u

def cmp_less_equal(t: int, u: int) -> bool:
    return t <= u

def cmp_greater_equal(t: int, u: int) -> bool:
    return t >= u

def in_range(t: int, minimum: int, maximum: int) -> bool:
    return minimum <= t <= maximum
