# cppset

A C++ style `std::set<T>` implementation (Ordered Unique Keys).

## Features
*   **Sorted**: Iteration always yields elements in ascending order.
*   **Unique**: Duplicates are ignored.
*   **Tree Underlying**: Implemented via Binary Search Tree nodes.
*   **Ops**: `lower_bound`, `upper_bound`, `insert`, `erase`.

## Usage
```python
from cppset import Set

s = Set([3, 1, 4, 1, 5, 9])
print(s) # Set({1, 3, 4, 5, 9}) -> Note sorted and unique

print(s.lower_bound(4)) # 4
print(s.upper_bound(4)) # 5
```
