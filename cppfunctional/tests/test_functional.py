import pytest
from cppfunctional import (
    Function, ReferenceWrapper, ref, cref, invoke,
    bind, bind_front, bind_back, _1, _2, _3
)

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

def test_bind():
    def subtract(a, b):
        return a - b
        
    bound_sub = bind(subtract, _1, _2)
    assert bound_sub(10, 5) == 5
    
    bound_sub_rev = bind(subtract, _2, _1)
    assert bound_sub_rev(10, 5) == -5
    
    bound_fixed = bind(subtract, 20, _1)
    assert bound_fixed(5) == 15

def test_bind_front_back():
    def mix(a, b, c):
        return a * 100 + b * 10 + c
        
    bf = bind_front(mix, 1, 2)
    assert bf(3) == 123
    
    bb = bind_back(mix, 2, 3)
    assert bb(1) == 123

