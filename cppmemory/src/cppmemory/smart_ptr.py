from typing import TypeVar, Generic, Optional, Any
import sys

T = TypeVar('T')

class ControlBlock(Generic[T]):
    """
    Shared state for shared_ptr and weak_ptr.
    """
    __slots__ = ('ptr', 'shared_count', 'weak_count')
    
    def __init__(self, ptr: Optional[T]):
        self.ptr = ptr
        self.shared_count = 1 if ptr is not None else 0
        self.weak_count = 0

class SharedPtr(Generic[T]):
    """
    Simulates std::shared_ptr.
    """
    __slots__ = ('_cb',)

    def __init__(self, ptr: Optional[T] = None, _cb: Optional[ControlBlock] = None):
        if _cb:
            self._cb = _cb
            if self._cb.ptr is not None:
                self._cb.shared_count += 1
        else:
            if ptr is not None:
                self._cb = ControlBlock(ptr)
            else:
                self._cb = None

    def __del__(self):
        self._decref()

    def _decref(self):
        if self._cb:
            self._cb.shared_count -= 1
            if self._cb.shared_count == 0:
                # Destruction of managed object
                self._cb.ptr = None
                # If weak_count is 0, we could technically let GC handle ControlBlock,
                # but standard semantics imply the object is gone.
            
            # Note: We rely on Python GC to clean up ControlBlock when shared_count + weak_count = 0 references to IT exist.
            # But the 'ptr' inside it is cleared when shared_count == 0.
            
    def get(self) -> Optional[T]:
        if self._cb:
            return self._cb.ptr
        return None

    def use_count(self) -> int:
        if self._cb:
            return self._cb.shared_count
        return 0

    def reset(self, ptr: Optional[T] = None):
        self._decref()
        if ptr is not None:
            self._cb = ControlBlock(ptr)
        else:
            self._cb = None

    def __bool__(self) -> bool:
        return self.get() is not None

    def __getattr__(self, name: str) -> Any:
        # Proxy access to underlying object
        obj = self.get()
        if obj is None:
            raise AttributeError("Accessing method on null shared_ptr")
        return getattr(obj, name)

    # Copy simulation: Python assignment is ref copy, so:
    # sp2 = sp1 does NOT call __init__. It just aliases.
    # To properly simulate shared_ptr copy semantics in Python, 
    # we need explicit copy or clone. 
    # BUT, since we share the ControlBlock, simple aliasing actually WORKS 
    # because they point to same ControlBlock instance!
    # Problem: __del__ only runs when Python object is garbage collected.
    # If we have 2 copies of SharedPtr object?
    # sp2 = sp1 (aliasing) -> 1 python object, 1 control block. use_count says 1? NO.
    # C++: shared_ptr p2 = p1; -> 2 distinct shared_ptr objects, ref_count=2.
    # Python: p2 = p1 -> 1 object.
    # Solution: We must implement `make_copy()` or copy constructor behavior.
    # Users effectively just pass shared_ptr around.
    # To truly simulate incrementing ref count, user must do `sp2 = SharedPtr(sp1)`?
    # Or `sp2 = sp1.copy()`
    
    def copy(self) -> 'SharedPtr[T]':
        """Creates a new SharedPtr sharing ownership."""
        return SharedPtr(_cb=self._cb)

class WeakPtr(Generic[T]):
    """
    Simulates std::weak_ptr.
    """
    __slots__ = ('_cb',)

    def __init__(self, sp: Optional[SharedPtr[T]] = None):
        if sp and sp._cb:
            self._cb = sp._cb
            self._cb.weak_count += 1
        else:
            self._cb = None

    def __del__(self):
        if self._cb:
            self._cb.weak_count -= 1

    def expired(self) -> bool:
        return self._cb is None or self._cb.shared_count == 0

    def lock(self) -> SharedPtr[T]:
        if self.expired():
            return SharedPtr() # Empty
        # Create new shared ptr from control block
        return SharedPtr(_cb=self._cb)

class UniquePtr(Generic[T]):
    """
    Simulates std::unique_ptr.
    Strictly owns the object. Not copyable.
    """
    __slots__ = ('_ptr',)

    def __init__(self, ptr: Optional[T] = None):
        self._ptr = ptr

    def get(self) -> Optional[T]:
        return self._ptr

    def release(self) -> Optional[T]:
        p = self._ptr
        self._ptr = None
        return p

    def reset(self, ptr: Optional[T] = None):
        # Delete old (handled by GC/assignment)
        self._ptr = ptr

    def __bool__(self) -> bool:
        return self._ptr is not None

    def __getattr__(self, name: str) -> Any:
        if self._ptr is None:
            raise AttributeError("Accessing method on null unique_ptr")
        return getattr(self._ptr, name)
    
    # Disable copy
    def __copy__(self):
        raise RuntimeError("unique_ptr is not copyable")
    
    def __deepcopy__(self, memo):
        raise RuntimeError("unique_ptr is not copyable")

def make_shared(cls, *args, **kwargs) -> SharedPtr:
    obj = cls(*args, **kwargs)
    return SharedPtr(obj)

def make_unique(cls, *args, **kwargs) -> UniquePtr:
    obj = cls(*args, **kwargs)
    return UniquePtr(obj)
