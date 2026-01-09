from typing import Any
import math
from .engine import RandomEngine, DefaultRandomEngine

class UniformIntDistribution:
    """Uniform integer distribution over [a, b]."""
    
    def __init__(self, a: int = 0, b: int = 2147483647):
        self._a = a
        self._b = b

    def __call__(self, engine: RandomEngine) -> int:
        return engine._randint(self._a, self._b)


class UniformRealDistribution:
    """Uniform real distribution over [a, b)."""
    
    def __init__(self, a: float = 0.0, b: float = 1.0):
        self._a = a
        self._b = b
    
    def __call__(self, engine: RandomEngine) -> float:
        r = engine._random()  # [0, 1)
        return self._a + r * (self._b - self._a)


class NormalDistribution:
    """Normal (Gaussian) distribution using Box-Muller transform.
    
    Warning: This class is NOT thread-safe. The Box-Muller implementation
    caches a spare value between calls. Use separate instances per thread.
    """
    
    def __init__(self, mean: float = 0.0, stddev: float = 1.0):
        self._mean = mean
        self._stddev = stddev
        self._has_spare = False
        self._spare = 0.0
    
    def __call__(self, engine: RandomEngine) -> float:
        # Box-Muller transform manual implementation if engine doesn't support gauss
        # DefaultRandomEngine is wrapper of random.Random, so we could use gauss() if exposed.
        # But for generic Engine support, we implement Box-Muller.
        
        if self._has_spare:
            self._has_spare = False
            return self._spare * self._stddev + self._mean
        
        while True:
            u = engine._random() * 2.0 - 1.0
            v = engine._random() * 2.0 - 1.0
            r = u*u + v*v
            if 0 < r < 1:
                break
        
        c = math.sqrt(-2.0 * math.log(r) / r)
        self._spare = v * c
        self._has_spare = True
        return (u * c) * self._stddev + self._mean

class BernoulliDistribution:
    def __init__(self, p: float = 0.5):
        self._p = p

    def __call__(self, engine: RandomEngine) -> bool:
        return engine._random() < self._p
