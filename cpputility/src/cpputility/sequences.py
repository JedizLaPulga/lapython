from typing import TypeVar, Generic, Tuple, Type, Any

T = TypeVar('T', int, bool)

class integer_sequence(Generic[T]):
    """
    Represents a compile-time sequence of integers.
    In Python, this is mostly a structural wrapper that holds the tuple of values.
    """
    __slots__ = ('_values', 'value_type')

    def __init__(self, value_type: Type[T], *args: T):
        self.value_type = value_type
        self._values: Tuple[T, ...] = args

    @property
    def size(self) -> int:
        return len(self._values)

    def __len__(self) -> int:
        return self.size

    def __iter__(self):
        return iter(self._values)

    def __repr__(self) -> str:
        vals = ", ".join(repr(x) for x in self._values)
        return f"integer_sequence({self.value_type.__name__}, {vals})"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, integer_sequence):
            return self.value_type == other.value_type and self._values == other._values
        return False

class index_sequence(integer_sequence[int]):
    """
    An integer_sequence where the type is int.
    """
    def __init__(self, *args: int):
        super().__init__(int, *args)
        
    def __repr__(self) -> str:
        vals = ", ".join(repr(x) for x in self._values)
        return f"index_sequence({vals})"

def make_integer_sequence(value_type: Type[T], n: int) -> integer_sequence[T]:
    if n < 0:
        raise ValueError("Sequence size must be non-negative")
    return integer_sequence(value_type, *(value_type(i) for i in range(n)))

def make_index_sequence(n: int) -> index_sequence:
    if n < 0:
        raise ValueError("Sequence size must be non-negative")
    return index_sequence(*range(n))

def index_sequence_for(*args: Any) -> index_sequence:
    return make_index_sequence(len(args))
