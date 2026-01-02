import pytest
from cpprandom import (
    DefaultRandomEngine, MT19937, LinearCongruentialEngine,
    UniformIntDistribution, UniformRealDistribution, NormalDistribution, BernoulliDistribution
)

def test_engines():
    mt = MT19937(42)
    val1 = mt()
    
    mt2 = MT19937(42)
    val2 = mt2()
    
    assert val1 == val2 # Deterministic scaling
    
    lcg = LinearCongruentialEngine(1)
    v1 = lcg()
    v2 = lcg()
    assert v1 != v2

def test_distributions():
    eng = DefaultRandomEngine(123)
    
    # Uniform Int
    u_int = UniformIntDistribution(1, 10)
    res = u_int(eng)
    assert 1 <= res <= 10
    
    # Uniform Real
    u_real = UniformRealDistribution(0.0, 1.0)
    f = u_real(eng)
    assert 0.0 <= f < 1.0
    
    # Bernoulli
    bern = BernoulliDistribution(0.5)
    b = bern(eng)
    assert isinstance(b, bool)

def test_normal_distribution():
    eng = DefaultRandomEngine(42)
    norm = NormalDistribution(0.0, 1.0)
    
    val = norm(eng)
    assert isinstance(val, float)
    
    # Check Box-Muller state (requires multiple calls)
    val2 = norm(eng)
    assert val != val2
