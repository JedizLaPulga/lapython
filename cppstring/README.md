# cppstring

> **C++ `std::string` for Python**

`cppstring` provides a mutable string class `String` that mimics the behavior of C++'s `std::string`. 
It allows in-place modification, dynamic resizing, and efficient character manipulation.

## Installation

```bash
pip install ./cppstring
```

## Usage

```python
from cppstring import String

s = String("Hello")
s.append(", World")
s.push_back('!')
print(s) # "Hello, World!"

s[0] = 'h' # Mutable!
print(s) # "hello, World!"

s.pop_back()
print(s.size()) # 12
```

## Features
*   **Mutable**: Modify characters in-place O(1).
*   **Dynamic**: `push_back`, `pop_back`, `append`, `insert`, `erase`.
*   **Compatible**: Iterable, Indexable, slicing support.
*   **Memory Managed**: `capacity`, `reserve`, `shrink_to_fit`.
