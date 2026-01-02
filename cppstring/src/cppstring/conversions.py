from typing import Union, Any
from .string import String

def to_string(val: Any) -> String:
    """Converts numeric value to String."""
    return String(str(val))

def stoi(s: Union[str, String], base: int = 10) -> int:
    """Parses string to int."""
    return int(str(s), base)

def stol(s: Union[str, String], base: int = 10) -> int:
    """Parses string to long (int in Python)."""
    return int(str(s), base)

def stoll(s: Union[str, String], base: int = 10) -> int:
    """Parses string to long long (int in Python)."""
    return int(str(s), base)

def stoul(s: Union[str, String], base: int = 10) -> int:
    """Parses string to unsigned long."""
    # Python doesn't handle unsigned/overflow manually unless we enforce it.
    # Just standard parse.
    return int(str(s), base)

def stoull(s: Union[str, String], base: int = 10) -> int:
    return int(str(s), base)

def stof(s: Union[str, String]) -> float:
    return float(str(s))

def stod(s: Union[str, String]) -> float:
    return float(str(s))

def stold(s: Union[str, String]) -> float:
    return float(str(s))
