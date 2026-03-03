from typing import TypeVar, Generic, Any

T = TypeVar('T')

class Ref(Generic[T]):
    __slots__ = ('_object',)
    
    def __init__(self, obj: T):
        self._object = obj
        
    def get(self) -> T:
        return self._object
        
    def __call__(self, *args, **kwargs) -> Any:
        return self._object(*args, **kwargs)

def ref(obj: T) -> Ref[T]:
    return Ref(obj)

def cref(obj: T) -> Ref[T]:
    return Ref(obj)
