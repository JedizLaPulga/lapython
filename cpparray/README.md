# cpparray

A C++ style fixed-size array implementation `std::array<T, N>` for Python.

## Features

- **Fixed Size**: Cannot be resized after creation.
- **Generic**: Works with any Python object.
- **Zero-Overhead Access**: Uses `ctypes` for contiguous memory storage of object references.
- **Strict API**: Matches C++ STL naming (`at()`, `front()`, `back()`, `fill()`, `size()`).

## Usage

```python
from cpparray import Array

# 1. Create array of size 5 filled with zeros
a = Array(5, init_value=0)
print(a) # Array[5]([0, 0, 0, 0, 0])

# 2. Initialize from list
b = Array(3, source=["a", "b", "c"])
print(b.front()) # 'a'

# 3. Modify
b[1] = "z"
b.at(2) # Safe access

# 4. Fill
a.fill(99)

# 5. Swap
a = Array(3, init_value=1)
b = Array(3, init_value=2)
a.swap(b) # Efficient swap
```

## Why use this?
When you want to communicate intent that a collection has a **fixed dimension** and should not grow or shrink, mimicking `std::array` semantics in algorithms.
