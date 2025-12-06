# cppunordered_set

A C++ style `std::unordered_set<T>` implementation.

## Features
*   **Hash Set**: Uses Separate Chaining (Buckets).
*   **Unique Keys**: Ignores duplicates.
*   **Interface**: `insert`, `erase`, `find`, `bucket_count`, `load_factor`.

## Usage
```python
from cppunordered_set import UnorderedSet

s = UnorderedSet()
s.insert(1)
s.insert(2)

if s.contains(1):
    print("Found 1")

print(f"Buckets: {s.bucket_count()}")
```
