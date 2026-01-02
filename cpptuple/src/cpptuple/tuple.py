from typing import Any, MutableSequence, overload, Iterable, Union, TypeVar, Generic, List

T = TypeVar('T')

class Tuple(MutableSequence[Any]):
    """
    A simplified mutable tuple implementation mimicking std::tuple.
    In C++, std::tuple is a fixed-size collection of heterogeneous values.
    Crucially, it is mutable (unless const), unlike Python's tuple.
    """
    __slots__ = ('_elements',)

    def __init__(self, *args: Any):
        # We store as list efficiently
        self._elements = list(args)

    # --------------------- Element Access ---------------------
    def __getitem__(self, index: Union[int, slice]) -> Any:
        return self._elements[index]

    def __setitem__(self, index: int, value: Any):
        # Allow mutation
        self._elements[index] = value

    def __delitem__(self, index: Union[int, slice]):
        # std::tuple is fixed size!
        # deletion is NOT supported in C++ tuple. 
        # But MutableSequence abstraction in Python usually implies it.
        # Strict C++ port: RAISE ERROR.
        raise TypeError("std::tuple is fixed-size. Cannot delete elements.")

    def __len__(self) -> int:
        return len(self._elements)

    def insert(self, index: int, value: Any):
        # Fixed size -> No insert
        raise TypeError("std::tuple is fixed-size. Cannot insert elements.")

    def swap(self, other: 'Tuple'):
        if len(self) != len(other):
            raise ValueError("Tuples must be same size to swap")
        self._elements, other._elements = other._elements, self._elements

    def __repr__(self) -> str:
        return f"Tuple({', '.join(repr(x) for x in self._elements)})"
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Tuple):
            return self._elements == other._elements
        if isinstance(other, tuple):
             return tuple(self._elements) == other
        return False
    
    def __lt__(self, other: 'Tuple') -> bool:
        if not isinstance(other, Tuple):
             return NotImplemented
        return self._elements < other._elements

    def __iter__(self):
        return iter(self._elements)

def make_tuple(*args: Any) -> Tuple:
    return Tuple(*args)

def get(index: int, t: Tuple) -> Any:
    return t[index]

def tuple_cat(*tuples: Tuple) -> Tuple:
    new_elems = []
    for t in tuples:
        new_elems.extend(t._elements)
    return Tuple(*new_elems)

def tie(*args):
    # tie is harder in Python because we don't have true references to simple vars.
    # We can't do x, y = 1, 2; tie(x, y) = some_tuple
    # and have x, y update.
    # Python does unpacking naturally: x, y = some_tuple[0], some_tuple[1]
    # So tie might be redundant or strictly for "Unpacking into mutable containers".
    # Skipping for now as it's not pythonic or easily doable without ref wrappers.
    pass
