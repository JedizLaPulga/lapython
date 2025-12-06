# cppdeque

A C++ style `std::deque` (double-ended queue) implementation for Python with O(1) random access.

Unlike Python's `collections.deque` (which is a linked list of blocks and has O(N) random access), `cppdeque` uses a **Map of Blocks** architecture (dynamic array of pointers to fixed-size blocks). This ensures:

1.  **O(1) Random Access**: `d[1000]` is constant time.
2.  **O(1) Push/Pop at ends**: Efficient growth at both front and back.
3.  **Fragmented Memory**: Large contiguous memory is not required (unlike `cppvector`), avoiding reallocation costs for huge datasets.

## Usage

```python
from cppdeque import Deque

d = Deque()

# Push back
d.push_back(10)

# Push front (efficient allocation)
d.push_front(5)

# O(1) Access
print(d[0]) # 5
print(d[1]) # 10

# Iteration
for x in d:
    print(x)
```
