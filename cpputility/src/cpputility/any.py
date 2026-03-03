from typing import Any as PyAny, Type, TypeVar

T = TypeVar('T')

class BadAnyCast(RuntimeError):
    pass

class Any:
    __slots__ = ('_value', '_has_value')
    
    def __init__(self, value: PyAny = None):
        if value is None:
            self._has_value = False
            self._value = None
        else:
            self._has_value = True
            self._value = value
            
    def has_value(self) -> bool:
        return self._has_value
        
    def type(self) -> Type:
        if not self._has_value:
            return type(None)
        return type(self._value)
        
    def reset(self) -> None:
        self._value = None
        self._has_value = False

def make_any(value: PyAny) -> Any:
    return Any(value)

def any_cast(any_obj: Any, type_to_cast: Type[T]) -> T:
    if not any_obj.has_value():
        raise BadAnyCast("Bad any_cast: empty Any")
    if not isinstance(any_obj._value, type_to_cast):
        raise BadAnyCast(f"Bad any_cast: expected {type_to_cast}, got {type(any_obj._value)}")
    return any_obj._value
