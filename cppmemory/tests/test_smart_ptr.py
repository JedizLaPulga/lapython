import pytest
from cppmemory import SharedPtr, WeakPtr, UniquePtr, make_shared, make_unique

class Resource:
    """Helper for checking destruction."""
    def __init__(self, val=0):
        self.val = val
        self.destroyed = False
    
    # We can't easily rely on __del__ in tests because of GC timing.
    # We rely on SharedPtr semantics (ref counts).

def test_shared_ptr_basic():
    sp = make_shared(Resource, 10)
    assert sp.use_count() == 1
    assert sp.val == 10
    
    sp2 = sp.copy() # Distinct shared_ptr sharing state
    assert sp2.use_count() == 2
    assert sp.use_count() == 2
    assert sp2.val == 10
    
    sp.reset()
    assert sp.get() is None
    assert sp2.use_count() == 1
    assert sp2.val == 10

def test_weak_ptr():
    sp = make_shared(Resource, 42)
    wp = WeakPtr(sp)
    
    assert not wp.expired()
    assert sp.use_count() == 1
    
    sp2 = wp.lock()
    assert sp2 is not None
    assert sp2.val == 42
    assert sp.use_count() == 2
    
    # Release strong refs
    sp2.reset()
    sp.reset()
    
    assert wp.expired()
    assert wp.lock().get() is None # Should return empty SharedPtr

def test_unique_ptr():
    up = make_unique(Resource, 100)
    assert up.val == 100
    
    # Move simulation -> release
    raw = up.release()
    assert raw.val == 100
    assert up.get() is None
    
    up.reset(raw)
    assert up.val == 100
    
    up.reset()
    assert up.get() is None

def test_shared_ptr_aliasing_behavior():
    # Verify our copy() logic
    # In C++, shared_ptr b = a; increments info.
    # In Python, b = a; is just reference copy.
    # users MUST use b = a.copy() to get a new SharedPtr object managing same resource
    # IF they want independent 'reset' capability on the shared_ptr wrapper itself.
    # If they use just b = a, calling b.reset() resets a too!
    
    sp1 = make_shared(Resource, 1)
    sp2 = sp1 # Aliasing
    sp2.reset()
    assert sp1.get() is None # They are the SAME object wrapper.
    
    sp3 = make_shared(Resource, 2)
    sp4 = sp3.copy() # New wrapper, same ControlBlock
    sp4.reset()
    assert sp4.get() is None
    assert sp3.get() is not None # sp3 wrapper still holds ref to ControlBlock
    assert sp3.use_count() == 1  # count decremented by sp4
