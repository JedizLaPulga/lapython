from typing import Union, TypeVar, Generic, Any
import math

class Duration:
    """
    Simulates std::chrono::duration.
    Stores count of ticks.
    """
    __slots__ = ('_count',)
    
    def __init__(self, count: Union[int, float] = 0):
        self._count = count

    def count(self) -> Union[int, float]:
        return self._count

    def zero(self):
        return Duration(0)
    
    def min(self):
        return Duration(-float('inf'))
    
    def max(self):
        return Duration(float('inf'))

    def __add__(self, other):
        if isinstance(other, Duration):
            return Duration(self._count + other._count)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Duration):
            return Duration(self._count - other._count)
        return NotImplemented
    
    def __mul__(self, scalar: Union[int, float]):
        return Duration(self._count * scalar)

    def __rmul__(self, scalar: Union[int, float]):
        return Duration(self._count * scalar)

    def __eq__(self, other):
        return isinstance(other, Duration) and self._count == other._count
    
    def __lt__(self, other):
        return isinstance(other, Duration) and self._count < other._count
        
    def __le__(self, other):
         return isinstance(other, Duration) and self._count <= other._count

    def __repr__(self):
        return f"Duration({self._count})"

# Helper typedefs/factories (Simulating different ratios)
# We will just use 'seconds' as base unit for simplicity in Python dynamic type?
# Or strict ratios? 
# C++: duration<int, ratio<1, 1000>> = milliseconds.
# Python: We can subclass or just assume specific units for the helpers.

class Nanoseconds(Duration):
    def __repr__(self): return f"{self._count}ns"

class Microseconds(Duration):
    def __repr__(self): return f"{self._count}us"

class Milliseconds(Duration):
    def __repr__(self): return f"{self._count}ms"

class Seconds(Duration):
    def __repr__(self): return f"{self._count}s"

class Minutes(Duration):
    def __repr__(self): return f"{self._count}m"

class Hours(Duration):
    def __repr__(self): return f"{self._count}h"

def nanoseconds(n) -> Nanoseconds: return Nanoseconds(n)
def microseconds(n) -> Microseconds: return Microseconds(n)
def milliseconds(n) -> Milliseconds: return Milliseconds(n)
def seconds(n) -> Seconds: return Seconds(n)
def minutes(n) -> Minutes: return Minutes(n)
def hours(n) -> Hours: return Hours(n)

# Duration cast logic?
# duration_cast<milliseconds>(seconds(1)) -> 1000ms.
# We need knowledge of ratio.
# Let's map ratios relative to Nanoseconds (ns).

_RATIOS = {
    Nanoseconds: 1,
    Microseconds: 1_000,
    Milliseconds: 1_000_000,
    Seconds: 1_000_000_000,
    Minutes: 60_000_000_000,
    Hours: 3600_000_000_000
}

def duration_cast(target_type, d: Duration):
    # This is rough dynamic casting simulation.
    # In C++ d comes with its own type. Here d is instance.
    source_type = type(d)
    
    if source_type not in _RATIOS:
        # Fallback for generic Duration, assume generic 'ticks' or seconds?
        # Let's assume generic Duration is seconds-based for convenience?
        # Or assume no conversion possible.
        if source_type == Duration:
             # Treat base Duration as seconds? Or raw?
             # Let's fail or default to source=1 (ns)?
             # Best to assume generic Duration is untyped ticks, can't cast without context.
             pass
    
    if target_type not in _RATIOS or source_type not in _RATIOS:
         # Just return generic
         return target_type(d.count())

    source_ns = d.count() * _RATIOS[source_type]
    target_count = source_ns // _RATIOS[target_type] # Integer division for cast
    return target_type(target_count)

