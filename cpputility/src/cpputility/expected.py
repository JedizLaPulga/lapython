from typing import TypeVar, Generic, Union, Any, cast

T = TypeVar('T')
E = TypeVar('E')

class Unexpected(Generic[E]):
    __slots__ = ('_error',)
    def __init__(self, error: E):
        self._error = error
        
    def error(self) -> E:
        return self._error

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Unexpected):
            return False
        return self._error == other._error

class BadExpectedAccess(RuntimeError):
    pass

class Expected(Generic[T, E]):
    __slots__ = ('_value', '_error', '_has_value')
    
    def __init__(self, value_or_unexpected: Union[T, Unexpected[E]]):
        if isinstance(value_or_unexpected, Unexpected):
            self._has_value = False
            self._error = value_or_unexpected.error()
            self._value = cast(T, None)
        else:
            self._has_value = True
            self._value = cast(T, value_or_unexpected)
            self._error = cast(E, None)
            
    def has_value(self) -> bool:
        return self._has_value
        
    def __bool__(self) -> bool:
        return self._has_value
        
    def value(self) -> T:
        if not self._has_value:
            raise BadExpectedAccess("Bad expected access: expected has no value")
        return self._value
        
    def error(self) -> E:
        if self._has_value:
            raise BadExpectedAccess("Bad expected access: expected has value, not error")
        return self._error
        
    def value_or(self, default_value: T) -> T:
        if self._has_value:
            return self._value
        return default_value
        
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Expected):
            return False
        if self._has_value != other._has_value:
            return False
        if self._has_value:
            return self._value == other._value
        return self._error == other._error
