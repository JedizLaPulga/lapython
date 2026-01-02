import time
from typing import Any
from .duration import Duration, Nanoseconds, Milliseconds, Seconds, duration_cast

class TimePoint:
    """
    Represents a point in time. 
    Stores duration since epoch.
    """
    __slots__ = ('_d',)
    
    def __init__(self, d: Duration):
        self._d = d
    
    def time_since_epoch(self) -> Duration:
        return self._d
    
    def __add__(self, other):
        if isinstance(other, Duration):
            return TimePoint(self._d + other)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, TimePoint):
             return self._d - other._d # Returns Duration
        if isinstance(other, Duration):
             return TimePoint(self._d - other)
        return NotImplemented

    def __eq__(self, other):
        return isinstance(other, TimePoint) and self._d == other._d
    
    def __lt__(self, other):
        return isinstance(other, TimePoint) and self._d < other._d

    def __repr__(self):
        return f"TimePoint({self._d})"

class SystemClock:
    """
    Wall clock time.
    """
    @staticmethod
    def now() -> TimePoint:
        # time.time_ns() returns ns since epoch
        ns = time.time_ns()
        return TimePoint(Nanoseconds(ns))
    
    @staticmethod
    def to_time_t(tp: TimePoint) -> float:
        d = duration_cast(Seconds, tp.time_since_epoch())
        return d.count()

class SteadyClock:
    """
    Monotonic clock.
    """
    @staticmethod
    def now() -> TimePoint:
        ns = time.monotonic_ns()
        return TimePoint(Nanoseconds(ns))

class HighResolutionClock(SteadyClock):
    pass
