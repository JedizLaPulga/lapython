from typing import Generic, TypeVar, Any, Union, Type, Callable

class BadVariantAccess(Exception):
    pass

class Variant:
    """
    A type-safe union container.
    Note: Python is dynamic, so Strict type checking against a predefined list of types
    is implied by usage of 'holds_alternative' or 'get'.
    """
    __slots__ = ('_value', '_index')
    
    def __init__(self, value: Any = None):
        self._value = value
        # Index is tricky without a fixed type list.
        # We'll rely on the value's type.
        
    def valueless_by_exception(self) -> bool:
        return False # Hard to achieve in Python unless we mess up assignment
        
    def index(self) -> int:
        return 0 # Meaningless without fixed type list
        
    def __repr__(self):
        return f"variant({self._value!r})"

    def __eq__(self, other):
        if isinstance(other, Variant):
            return self._value == other._value
        return self._value == other

def holds_alternative(v: Variant, t: Type) -> bool:
    return isinstance(v._value, t)

def get(v: Variant, t: Type) -> Any:
    if not isinstance(v._value, t):
        raise BadVariantAccess(f"Variant does not hold type {t}")
    return v._value

def get_if(v: Variant, t: Type) -> Any:
    """Returns value if type matches, else None."""
    if isinstance(v._value, t):
        return v._value
    return None

def visit(visitor: Callable[[Any], Any], v: Variant) -> Any:
    return visitor(v._value)
