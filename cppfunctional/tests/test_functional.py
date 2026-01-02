import pytest
from cppfunctional import Function, ReferenceWrapper, ref, cref, invoke

def add(a, b):
    return a + b

class Adder:
    def __init__(self, val):
        self.val = val
    def __call__(self, x):
        return self.val + x

def test_reference_wrapper():
    x = 10
    r = ref(x)
    assert r.get() == 10
    
    # In python simple items don't ref update (int is immutable).
    # But mutable type:
    lst = [1, 2]
    r_lst = ref(lst)
    lst.append(3)
    assert r_lst.get() == [1, 2, 3]

def test_function():
    f = Function(add)
    assert f(2, 3) == 5
    
    # Lambda
    f2 = Function(lambda x: x * 2)
    assert f2(10) == 20
    
    # Empty
    f_empty = Function(None)
    assert not f_empty
    with pytest.raises(RuntimeError):
        f_empty()

def test_invoke():
    assert invoke(add, 2, 3) == 5
    
    adder = Adder(10)
    assert invoke(adder, 5) == 15
    
    # Invoke with ref
    r_adder = ref(adder)
    assert invoke(r_adder, 5) == 15
