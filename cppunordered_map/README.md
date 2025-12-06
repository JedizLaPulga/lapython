# cppunordered_map

A C++ style `std::unordered_map` implementation.

## Features
*   **Separate Chaining**: Unlike Python's `dict` (Open Addressing), this uses linked lists (buckets) for collision resolution, strictly matching C++'s standard behavior (e.g. valid pointers to elements after rehash if we had pointers).
*   **Bucket Interface**: Exposes `bucket_count()`, `bucket_size(n)`, `load_factor()`.
*   **Rehashing Control**: `max_load_factor()`.

## Usage
```python
from cppunordered_map import UnorderedMap

m = UnorderedMap()
m["key"] = "value"

# Check internal structure
print(f"Buckets: {m.bucket_count()}")
print(f"Load Factor: {m.load_factor()}")

# Force rehash
m.max_load_factor(0.5)
```
