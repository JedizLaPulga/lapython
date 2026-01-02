from typing import Union, Optional, Any
from .string import String

class StringView:
    """
    A non-owning reference to a string or substring.
    Mimics C++17 std::string_view.
    """
    __slots__ = ('_source', '_start', '_len')

    def __init__(self, source: Union[str, String, 'StringView'], offset: int = 0, count: int = -1):
        if isinstance(source, StringView):
            self._source = source._source
            base_start = source._start
            base_len = source._len
        else:
            self._source = source
            base_start = 0
            base_len = len(source)
        
        if offset < 0:
            offset = 0 # Match C++ behavior? C++ throws out_of_range if pos > size.
        
        if offset > base_len:
            # In C++ constructor, if pos > size, it throws.
            # Here we clamp or throw? Let's throw to match C++ strictness or valid python slicing?
            # C++: string_view(const char* s, count) -> View first count.
            # string_view(string& s) -> View whole.
            # substr matches C++. 
            # Constructor usually takes pointer and length.
            # Let's assume this handles the logic: view(source, offset, count)
            # effectively source.substr(offset, count) as a view.
            offset = base_len # Empty view
        
        self._start = base_start + offset
        
        max_len = base_len - offset
        if count == -1 or count > max_len:
            self._len = max_len
        else:
            self._len = count

    def __len__(self) -> int:
        return self._len

    def empty(self) -> bool:
        return self._len == 0

    def at(self, index: int) -> str:
        if index < 0 or index >= self._len:
            raise IndexError("StringView index out of range")
        return self._source[self._start + index]

    def __getitem__(self, index: Union[int, slice]) -> Union[str, 'StringView']:
        if isinstance(index, slice):
            start, stop, step = index.indices(self._len)
            if step != 1:
                # StringView doesn't support stride != 1 efficiently without copying
                # Return string? Or fail?
                # C++ doesn't have strided view.
                # Let's return a new StringView if step is 1, else raise/copy.
                raise ValueError("StringView does not support strided slicing")
            
            # New view relative to this one
            new_offset = start # relative to 0 of this view
            new_count = stop - start
            return StringView(self._source, self._start + new_offset - (self._source._start if isinstance(self._source, StringView) else 0), new_count) 
            # Wait, recursion in logic. Simpler:
            # We are creating a NEW view.
            # Pass THIS view as source?
            return StringView(self, start, stop - start)

        if index < 0: index += self._len
        if not (0 <= index < self._len):
            raise IndexError("StringView index out of range")
        return self._source[self._start + index]

    def __str__(self) -> str:
        # Materialize
        if isinstance(self._source, str):
            return self._source[self._start : self._start + self._len]
        # String object
        # We can implement a bulk fetch if String supports it, or looping
        # String.substr returns a String (copy).
        # We want a python str.
        # String.c_str() returns full string.
        # If String exposes slicing that returns str, use that?
        # String slice returns String.
        # Let's iterate.
        return "".join([self._source[self._start + i] for i in range(self._len)])
    
    def to_string(self) -> String:
        return String(str(self))

    def remove_prefix(self, n: int):
        if n > self._len:
            n = self._len
        self._start += n
        self._len -= n

    def remove_suffix(self, n: int):
        if n > self._len:
            n = self._len
        self._len -= n

    def starts_with(self, prefix: Union[str, String, 'StringView']) -> bool:
        return str(self).startswith(str(prefix))

    def ends_with(self, suffix: Union[str, String, 'StringView']) -> bool:
        return str(self).endswith(str(suffix))
    
    def substr(self, pos: int = 0, count: int = -1) -> 'StringView':
        if pos >= self._len:
            return StringView(self, self._len, 0)
        return StringView(self, pos, count)
