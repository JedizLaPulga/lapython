from typing import Generic, TypeVar, Any, Tuple, Union

T1 = TypeVar('T1')
T2 = TypeVar('T2')

class Pair(Generic[T1, T2]):
    __slots__ = ('first', 'second')
    
    def __init__(self, first: T1 = None, second: T2 = None):
        self.first = first
        self.second = second
        
    def swap(self, other: 'Pair[T1, T2]'):
        self.first, other.first = other.first, self.first
        self.second, other.second = other.second, self.second
        
    # --------------------- Comparisons ---------------------
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Pair):
            return self.first == other.first and self.second == other.second
        if isinstance(other, tuple) and len(other) == 2:
            return self.first == other[0] and self.second == other[1]
        return NotImplemented

    def __lt__(self, other: 'Pair[T1, T2]') -> bool:
        if not isinstance(other, Pair): return NotImplemented
        if self.first < other.first: return True
        if other.first < self.first: return False
        return self.second < other.second
        
    def __le__(self, other: 'Pair[T1, T2]') -> bool:
        return not (other < self)

    def __gt__(self, other: 'Pair[T1, T2]') -> bool:
        return other < self
        
    def __ge__(self, other: 'Pair[T1, T2]') -> bool:
        return not (self < other)

    # --------------------- Python Protocols ---------------------
    def __repr__(self) -> str:
        return f"pair({self.first!r}, {self.second!r})"
        
    def __iter__(self):
        """Allows unpacking: a, b = Pair(1, 2)"""
        yield self.first
        yield self.second
        
    def __hash__(self):
        return hash((self.first, self.second))

def make_pair(t1: T1, t2: T2) -> Pair[T1, T2]:
    return Pair(t1, t2)
