# cppinplace_vector

A Python implementation of the C++26 `std::inplace_vector`.

`inplace_vector` is a dynamically-resizable vector with a fixed capacity known at creation time. It provides a way to use vector-like semantics without dynamic memory allocation beyond the initial pre-allocation (or stack allocation in C++ terms).

## Usage

```python
from cppinplace_vector import InplaceVector

# Create a vector with fixed capacity of 3
v = InplaceVector(3)

v.push_back(10)
v.push_back(20)
v.push_back(30)

# v.push_back(40) # Raises MemoryError (bad_alloc equivalent)

if not v.try_push_back(50):
    print("Full!")

print(v.size()) # 3
print(v.max_size()) # 3
```
