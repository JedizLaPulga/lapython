# cppvector

A C++ style vector implementation for Python.

## Installation

```bash
pip install cppvector
```

## Usage

```python
from cppvector import Vector

# Create a vector
v = Vector()

# Add elements
v.push_back(1)
v.push_back(2)
v.push_back(3)

# Access elements
print(v[0])  # Output: 1

# Size and capacity
print(v.size())
print(v.capacity())
```

## Features

- Dynamic array with automatic resizing
- C++ STL vector-like interface
- Efficient memory management

## License

MIT License
