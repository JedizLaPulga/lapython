from typing import TypeVar, Generic, Any, Callable, Union, Optional
import functools

T = TypeVar('T')

class ReferenceWrapper(Generic[T]):
    """
    Simulates std::reference_wrapper.
    Wraps an object reference.
    """
    __slots__ = ('_obj',)

    def __init__(self, obj: T):
        # Prevent double wrapping? C++ doesn't, but useful.
        # But we must allow wrapping ReferenceWrapper as per std.
        self._obj = obj

    def get(self) -> T:
        return self._obj

    def __call__(self, *args, **kwargs) -> Any:
        return self._obj(*args, **kwargs)

    def __repr__(self):
        return f"ref({repr(self._obj)})"

def ref(obj: T) -> ReferenceWrapper[T]:
    return ReferenceWrapper(obj)

def cref(obj: T) -> ReferenceWrapper[T]:
    # In Python, const is convention. We just return a ReferenceWrapper.
    return ReferenceWrapper(obj)

class Function:
    """
    Simulates std::function.
    Wraps any callable.
    """
    __slots__ = ('_callable',)

    def __init__(self, fn: Callable):
        if fn is None:
             self._callable = None
        else:
             self._callable = fn

    def __call__(self, *args, **kwargs):
        if self._callable is None:
            raise RuntimeError("std::function called with empty target")
        return self._callable(*args, **kwargs)

    def __bool__(self):
        return self._callable is not None
    
    def target(self) -> Optional[Callable]:
        return self._callable

def invoke(f: Any, *args, **kwargs) -> Any:
    """
    Simulates std::invoke.
    """
    # 1. Pointer to member function (simulated by Method string name? No, direct function)
    # Python methods are callables.
    # 1. f is ReferenceWrapper
    if isinstance(f, ReferenceWrapper):
        return f(*args, **kwargs)
    
    # 2. Member function? In python usually obj.method.
    # If users pass (method_name, obj), we could support it.
    # C++: invoke(&Class::method, obj, args...)
    # We'll stick to standard callable support + ref wrapper.
    return f(*args, **kwargs)
