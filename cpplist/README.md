# cpplist

A C++ style doubly linked list implementation for Python.

## Installation

```bash
pip install cpplist-jediz
```

## Basic Usage

```python
from cpplist import List

# 1. Create and push
l = List([1, 2, 3])
l.push_back(4)
l.push_front(0)
print("List:", l)  # List[5](0, 1, 2, 3, 4)

# 2. Modifiers
l.pop_back()
l.pop_front()
l.insert(2, 99)  # Insert 99 at index 2
print("Modified:", l)

# 3. Swap
l2 = List([10, 20])
l.swap(l2)
print("After swap - l:", l)
print("After swap - l2:", l2)
```

## Features

- Doubly Linked List structure
- C++ STL list-like interface (push_back, push_front, insert, erase, etc.)
- O(1) push/pop front/back
- Memory optimized nodes using `__slots__`

## License

MIT License
