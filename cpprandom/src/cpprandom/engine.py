import random
from typing import Optional
from abc import ABC, abstractmethod

class RandomEngine(ABC):
    """Abstract base interface for random engines."""
    
    @abstractmethod
    def __call__(self) -> int:
        """Generate next random number."""
        ...
    
    @abstractmethod
    def min(self) -> int:
        """Return minimum possible value."""
        ...
    
    @abstractmethod
    def max(self) -> int:
        """Return maximum possible value."""
        ...

class DefaultRandomEngine(RandomEngine):
    """
    Wrapper around Python's random.Random (Mersenne Twister).
    NOTE: Python's random is already MT19937 based.
    """
    def __init__(self, seed: Optional[int] = None):
        self._rng = random.Random(seed)
        
    def __call__(self) -> int:
        # C++ default_random_engine range is implementation defined, often [0, RAND_MAX] or [0, 2^32-1].
        # We'll use 32-bit uint range for standard simulation.
        return self._rng.getrandbits(32)
    
    def min(self) -> int: return 0
    def max(self) -> int: return 2**32 - 1
    
    def seed(self, val: int):
        self._rng.seed(val)

    # Internal helper for distributions to get float [0, 1)
    def _random(self) -> float:
        return self._rng.random()
    
    def _randint(self, a, b) -> int:
        return self._rng.randint(a, b)

class MT19937(DefaultRandomEngine):
    """
    Mersenne Twister 19937.
    """
    # Python random IS MT19937.
    pass

class LinearCongruentialEngine(RandomEngine):
    """
    Simple LCG implementation.
    """
    def __init__(self, seed: int = 1):
        self._state = seed
        # std::minstd_rand parameters:
        self._a = 48271
        self._m = 2147483647 # 2^31 - 1
        self._c = 0
    
    def __call__(self) -> int:
        self._state = (self._a * self._state + self._c) % self._m
        return self._state
    
    def min(self) -> int: return 1
    def max(self) -> int: return self._m - 1
    
    def seed(self, val: int):
        self._state = val
    
    # Helpers for distributions (inefficient for LCG but working)
    def _random(self) -> float:
        return self() / self.max()
    
    def _randint(self, a, b) -> int:
        # Naive implementation
        r = self()
        span = b - a + 1
        return a + (r % span)

