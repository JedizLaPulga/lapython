from typing import Generic, TypeVar, Any, Union, NoReturn

T = TypeVar('T')

class NullOptType:
    def __repr__(self): return "nullopt"

nullopt = NullOptType()

class Optional(Generic[T]):
    __slots__ = ('_value', '_active')
    
    def __init__(self, value: Union[T, NullOptType] = nullopt):
        if value is nullopt:
            self._active = False
            self._value = None
        else:
            self._active = True
            self._value = value
            
    def has_value(self) -> bool:
        return self._active
        
    def __bool__(self) -> bool:
        return self._active
        
    def value(self) -> T:
        if not self._active:
            raise RuntimeError("Bad optional access")
        return self._value
        
    def value_or(self, default: T) -> T:
        if self._active:
            return self._value
        return default
        
    def reset(self):
        self._active = False
        self._value = None
        
    def emplace(self, value: T) -> T:
        """Constructs value in-place. In Python, this simply assigns the value.
        
        For C++ semantics where emplace constructs via args, use:
            opt.emplace(MyClass(arg1, arg2))
        
        Returns the emplaced value.
        """
        self._value = value
        self._active = True
        return self._value
        
    def swap(self, other: 'Optional[T]'):
        self._value, other._value = other._value, self._value
        self._active, other._active = other._active, self._active

    # --------------------- Operators ---------------------
    def __eq__(self, other: Any) -> bool:
        if other is nullopt:
            return not self._active
        if isinstance(other, Optional):
            if not self._active and not other._active: return True
            if self._active and other._active: return self._value == other._value
            return False
        # Compare with T
        if self._active: return self._value == other
        return False
        
    def __lt__(self, other: Any) -> bool:
        if other is nullopt:
            return False # nullopt < any active is True (nullopt comes first)
        if isinstance(other, Optional):
            if not self._active: return other._active
            if not other._active: return False
            return self._value < other._value
        # Compare with T
        if not self._active: return True # nullopt < value
        return self._value < other

    def __repr__(self):
        if self._active:
            return f"optional({self._value!r})"
        return "nullopt"

def make_optional(value: T) -> Optional[T]:
    return Optional(value)
