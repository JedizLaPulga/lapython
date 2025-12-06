# cppbitset

A C++ style `std::bitset<N>` implementation.

## Usage

```python
from cppbitset import Bitset

# 1. Create a bitset of 8 bits, initialized to 5
b = Bitset(8, 5) 
print(b) # bitset<8>(00000101)

# 2. Access and modify
print(b[0]) # True (LSB is 1)
print(b[1]) # False
b.flip(1)
print(b[1]) # True

# 3. Bitwise Ops
b2 = Bitset(8, "11111111")
result = b & b2
print(result)

# 4. Count
print(b.count()) # Number of set bits
```

## Features
*   **Space Efficient**: Values stored as a single Python integer.
*   **Fixed Size**: Operations respect the bit count (shifts truncate, init truncates).
*   **API**: `set`, `reset`, `flip`, `test`, `to_string`, `to_ulong`.
