import pytest
from cpptuple import Tuple, make_tuple, get, tuple_cat

def test_tuple_creation():
    t = Tuple(1, "hello", 3.14)
    assert len(t) == 3
    assert t[0] == 1
    assert t[1] == "hello"
    
    t2 = make_tuple(1, 2, 3)
    assert t2 == Tuple(1, 2, 3)

def test_tuple_mutability():
    t = Tuple(1, 2, 3)
    t[1] = 99
    assert t[1] == 99
    assert t == Tuple(1, 99, 3)

def test_tuple_fixed_size():
    t = Tuple(1, 2)
    with pytest.raises(TypeError):
        del t[0]
    
    with pytest.raises(TypeError):
        t.insert(0, 99)
        
    with pytest.raises(TypeError):
        t.append(5)
        # Wait, MutableSequence provides append based on insert/len.
        # If we raise in insert, append should fail.
        # Let's verify standard list methods don't work or raise.

def test_get():
    t = Tuple(10, 20)
    assert get(0, t) == 10
    assert get(1, t) == 20

def test_tuple_cat():
    t1 = Tuple(1, 2)
    t2 = Tuple(3, 4)
    t3 = tuple_cat(t1, t2)
    assert len(t3) == 4
    assert t3 == Tuple(1, 2, 3, 4)
    
    # Original untouched?
    assert t1 == Tuple(1, 2)

def test_swap():
    t1 = Tuple(1, 2)
    t2 = Tuple(8, 9)
    t1.swap(t2)
    
    assert t1 == Tuple(8, 9)
    assert t2 == Tuple(1, 2)

def test_repr():
    t = Tuple(1, 'a')
    assert repr(t) == "Tuple(1, 'a')"
