from __future__ import annotations
from typing import Union, Iterable, Iterator, Any, overload
import ctypes
from cppbase import Sequence

class String(Sequence):
    """
    A mutable, C++ style string implementation for Python.
    Supports SSO (Small String Optimization) and strict memory management.
    """
    _SSO_CAP = 15  # std::string usually has 15 chars SSO (16 bytes struct)
    __slots__ = ('_size', '_capacity', '_is_small', '_small', '_large')

    def __init__(self, source: Union[str, Iterable[str], 'String', None] = None):
        self._size = 0
        self._capacity = self._SSO_CAP
        self._is_small = True
        
        # Small buffer: Fixed size list
        self._small = [None] * (self._SSO_CAP + 1) 
        self._large = None
        
        if source is not None:
            self.assign(source)

    # --------------------- Internal ---------------------
    def _move_to_large(self, new_cap: int):
        if not self._is_small:
            return
        
        # Allocate large buffer using ctypes
        new_cap = max(new_cap, 32)
        large = (ctypes.py_object * new_cap)()
        
        for i in range(self._size):
            large[i] = self._small[i]
            
        self._large = large
        self._capacity = new_cap
        self._is_small = False
        self._small = None # Release small buffer

    def _resize_capacity(self, new_cap: int):
        if self._is_small and new_cap <= self._SSO_CAP:
            return
        if self._is_small:
            self._move_to_large(new_cap)
            return
        
        if new_cap == self._capacity:
            return
            
        # Realloc large
        new_data = (ctypes.py_object * new_cap)()
        for i in range(self._size):
            new_data[i] = self._large[i]
            
        self._large = new_data
        self._capacity = new_cap

    def _validate_char(self, c: Any) -> str:
        if isinstance(c, str):
            if len(c) == 1:
                return c
            raise ValueError(f"String can only contain single characters, got length {len(c)}")
        raise TypeError(f"String requires str characters, got {type(c)}")

    # --------------------- Modifiers ---------------------
    def assign(self, source: Union[str, Iterable[str], 'String']):
        self.clear()
        self.append(source)

    def append(self, source: Union[str, Iterable[str], 'String']):
        if isinstance(source, String):
            for char in source:
                self.push_back(char)
        elif isinstance(source, str):
            for char in source:
                self.push_back(char)
        else:
            for char in source:
                self.push_back(char)

    def push_back(self, c: str):
        val = self._validate_char(c)
        
        if self._size == self._capacity:
            # Growth factor 2x
            self._resize_capacity(self._capacity * 2)
            
        if self._is_small:
            self._small[self._size] = val
        else:
            self._large[self._size] = val
            
        self._size += 1

    def pop_back(self):
        if self._size == 0:
            raise IndexError("pop_back on empty string")
        self._size -= 1
        # Optional: null out for GC, though strings are small
        if self._is_small:
            self._small[self._size] = None
        else:
            self._large[self._size] = None

    def insert(self, pos: int, sub: str):
        if pos < 0: pos += self._size
        if not (0 <= pos <= self._size):
            raise IndexError("insert index out of range")
        
        sub_len = len(sub)
        if self._size + sub_len > self._capacity:
            self._resize_capacity(max(self._size + sub_len, self._capacity * 2))
            
        # Shift
        # We need to shift starting from end
        # Python range is strict, so we do it carefully or just use list slice logic if we weren't doing manual memory compliance
        
        # Accessor helper
        tgt = self._small if self._is_small else self._large
        
        # Shift right
        for i in range(self._size - 1, pos - 1, -1):
            tgt[i + sub_len] = tgt[i]
            
        # Insert
        for i, char in enumerate(sub):
            tgt[pos + i] = char
            
        self._size += sub_len

    def erase(self, pos: int = 0, count: int = -1) -> 'String':
        """Removes count characters starting from pos (default to end). returns self."""
        if pos < 0 or pos >= self._size:
            raise IndexError("erase index out of range")
            
        if count == -1:
            count = self._size - pos
            
        if pos + count > self._size:
            count = self._size - pos
            
        tgt = self._small if self._is_small else self._large
        
        # Shift left
        for i in range(pos + count, self._size):
            tgt[i - count] = tgt[i]
            
        self._size -= count
        return self

    def clear(self):
        self._size = 0

    def replace(self, pos: int, count: int, sub: str) -> 'String':
        self.erase(pos, count)
        self.insert(pos, sub)
        return self

    def swap(self, other: 'String'):
        if not isinstance(other, String):
            raise TypeError("Can only swap with another String")
        
        (self._size, other._size) = (other._size, self._size)
        (self._capacity, other._capacity) = (other._capacity, self._capacity)
        (self._is_small, other._is_small) = (other._is_small, self._is_small)
        (self._small, other._small) = (other._small, self._small)
        (self._large, other._large) = (other._large, self._large)

    # --------------------- Element Access ---------------------
    def __getitem__(self, index: Union[int, slice]) -> Union[str, 'String']:
        if isinstance(index, slice):
            start, stop, step = index.indices(self._size)
            res = String()
            src = self._small if self._is_small else self._large
            for i in range(start, stop, step):
                res.push_back(src[i])
            return res
        
        if index < 0: index += self._size
        if not (0 <= index < self._size):
            raise IndexError("String index out of range")
        
        return (self._small if self._is_small else self._large)[index]

    def __setitem__(self, index: int, value: str):
        if index < 0: index += self._size
        if not (0 <= index < self._size):
            raise IndexError("String index out of range")
        
        val = self._validate_char(value)
        (self._small if self._is_small else self._large)[index] = val

    def at(self, index: int) -> str:
        return self[index]
    
    def front(self) -> str:
        return self[0]
    
    def back(self) -> str:
        return self[self._size - 1]
    
    def c_str(self) -> str:
        """Returns native Python string."""
        if self._size == 0:
            return ""
        src = self._small if self._is_small else self._large
        # Efficient join of py_objects
        # We need to extract them to a list first because join expects iterator
        # slicing a ctypes array might not work directly with join
        return "".join([src[i] for i in range(self._size)])

    def __str__(self) -> str:
        return self.c_str()

    def __repr__(self) -> str:
        return f'String("{self.c_str()}")'

    # --------------------- Capacity ---------------------
    def size(self) -> int: return self._size
    def length(self) -> int: return self._size
    def empty(self) -> bool: return self._size == 0
    def capacity(self) -> int: return self._capacity
    
    def reserve(self, n: int):
        if n > self._capacity:
            self._resize_capacity(n)

    def resize(self, n: int, c: str = '\0'):
        if n < self._size:
            self._size = n
            # Data remains but is inaccessible, strictly safe.
        elif n > self._size:
            if n > self._capacity:
                self.reserve(n)
            
            val = self._validate_char(c)
            tgt = self._small if self._is_small else self._large
            for i in range(self._size, n):
                tgt[i] = val
            self._size = n

    def shrink_to_fit(self):
        if self._is_small:
            return
        if self._size <= self._SSO_CAP:
            # Move back to small
            small = [None] * (self._SSO_CAP + 1)
            for i in range(self._size):
                small[i] = self._large[i]
            self._small = small
            self._large = None
            self._is_small = True
            self._capacity = self._SSO_CAP
        elif self._size < self._capacity:
            self._resize_capacity(self._size)

    # --------------------- Operations ---------------------
    def __add__(self, other: Union[str, 'String']) -> 'String':
        s = String(self)
        s.append(other)
        return s

    def __iadd__(self, other: Union[str, 'String']) -> 'String':
        self.append(other)
        return self

    def substr(self, pos: int = 0, count: int = -1) -> 'String':
        if pos < 0 or pos > self._size:
            raise IndexError("pos out of range")
        if count == -1 or pos + count > self._size:
            count = self._size - pos
        
        # Use existing slice logic
        return self[pos : pos + count]

    def find(self, sub: str, pos: int = 0) -> int:
        # Optimization: To avoid building huge strings, check first char then compare
        # But native string search is extremely optimized.
        # For now, convert to string and search.
        s = self.c_str()
        return s.find(sub, pos)

    def rfind(self, sub: str, pos: int = -1) -> int:
        s = self.c_str()
        if pos == -1:
            return s.rfind(sub)
        return s.rfind(sub, 0, pos + len(sub)) # Adjusting pos to match C++ behavior semantics closely or assume standard python rfind?
        # C++ rfind(str, pos) searches for last occurrence at or BEFORE pos.
        # Python rfind(str, start, end) searches within range.
        # If pos is provided in C++, it effectively means "ignore anything after index pos"
        # So in Python it corresponds to end=pos + len(sub)? Or something.
        # Let's just use Python defaults.
        return s.rfind(sub, 0, pos if pos != -1 else None)

    def compare(self, other: Union[str, 'String']) -> int:
        s = self.c_str()
        o = str(other)
        if s < o: return -1
        if s > o: return 1
        return 0

    def find_first_of(self, chars: str, pos: int = 0) -> int:
        """Finds the first occurrence of any character from the set."""
        if pos < 0: pos += self._size
        if pos < 0: pos = 0
        
        src = self._small if self._is_small else self._large
        charset = set(chars)
        for i in range(pos, self._size):
            if src[i] in charset:
                return i
        return -1

    def find_last_of(self, chars: str, pos: int = -1) -> int:
        """Finds the last occurrence of any character from the set at or before pos."""
        if pos == -1 or pos >= self._size:
            pos = self._size - 1
        elif pos < 0:
            pos += self._size
        
        if pos < 0: return -1 # Still negative? Empty or out of bounds

        src = self._small if self._is_small else self._large
        charset = set(chars)
        for i in range(pos, -1, -1):
            if src[i] in charset:
                return i
        return -1

    def find_first_not_of(self, chars: str, pos: int = 0) -> int:
        """Finds the first occurrence of any character NOT from the set."""
        if pos < 0: pos += self._size
        if pos < 0: pos = 0
        
        src = self._small if self._is_small else self._large
        charset = set(chars)
        for i in range(pos, self._size):
            if src[i] not in charset:
                return i
        return -1

    def find_last_not_of(self, chars: str, pos: int = -1) -> int:
        """Finds the last occurrence of any character NOT from the set at or before pos."""
        if pos == -1 or pos >= self._size:
            pos = self._size - 1
        elif pos < 0:
            pos += self._size
            
        if pos < 0: return -1

        src = self._small if self._is_small else self._large
        charset = set(chars)
        for i in range(pos, -1, -1):
            if src[i] not in charset:
                return i
        return -1

    # --------------------- Case Conversions ---------------------
    def to_upper(self) -> 'String':
        """Converts string to uppercase in-place."""
        # Using c_str() and assign() ensures correct handling of characters that change length (e.g. 'ß')
        self.assign(self.c_str().upper())
        return self

    def to_lower(self) -> 'String':
        """Converts string to lowercase in-place."""
        self.assign(self.c_str().lower())
        return self


    # --------------------- Comparisons ---------------------
    def __eq__(self, other: object) -> bool:
        if isinstance(other, (String, str)):
            return self.compare(other) == 0
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        if isinstance(other, (String, str)):
            return self.compare(other) != 0
        return NotImplemented

    def __lt__(self, other: Union[String, str]) -> bool:
        if isinstance(other, (String, str)):
            return self.compare(other) < 0
        return NotImplemented

    def __le__(self, other: Union[String, str]) -> bool:
        if isinstance(other, (String, str)):
            return self.compare(other) <= 0
        return NotImplemented

    def __gt__(self, other: Union[String, str]) -> bool:
        if isinstance(other, (String, str)):
            return self.compare(other) > 0
        return NotImplemented

    def __ge__(self, other: Union[String, str]) -> bool:
        if isinstance(other, (String, str)):
            return self.compare(other) >= 0
        return NotImplemented

    # --------------------- Predicates (C++20) ---------------------
    def starts_with(self, prefix: Union[str, 'String', 'StringView']) -> bool:
        # Avoid circular import if possible, explicit check
        p_str = str(prefix)
        if self._size < len(p_str):
            return False
        # Optimization: check directly
        return self.c_str().startswith(p_str)

    def ends_with(self, suffix: Union[str, 'String', 'StringView']) -> bool:
        s_str = str(suffix)
        return self.c_str().endswith(s_str)

    def contains(self, sub: Union[str, 'String', 'StringView']) -> bool:
        return self.find(str(sub)) != -1

    # --------------------- Iteration ---------------------
    def __iter__(self) -> Iterator[str]:
        src = self._small if self._is_small else self._large
        for i in range(self._size):
            yield src[i]
    
    def __len__(self) -> int:
        return self._size

