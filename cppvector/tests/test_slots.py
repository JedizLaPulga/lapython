
import pytest
from cppvector.vector import Vector, VectorBool, NumericVector

def test_vector_slots():
    v = Vector()
    # verify slots exist
    assert hasattr(v, '__slots__')
    # verify we cannot add arbitrary attributes
    with pytest.raises(AttributeError):
        v.new_attr = 10

def test_vector_bool_slots():
    vb = VectorBool()
    assert hasattr(vb, '__slots__')
    with pytest.raises(AttributeError):
        vb.new_attr = 10

def test_numeric_vector_slots():
    nv = NumericVector()
    assert hasattr(nv, '__slots__')
    with pytest.raises(AttributeError):
        nv.new_attr = 10
