# cpphive

A Python implementation of the C++ `plf::hive` (also known as `std::hive` proposal) container.

It is a bucket-array based container that provides:
- Stability of iterators/references upon insertion and erasure.
- O(1) insertion and erasure (amortized).
- Fast iteration (skipping erased elements).

## Usage

```python
from cpphive import Hive

h = Hive()
it1 = h.insert(10)
it2 = h.insert(20)
h.insert(30)

print(list(h)) # [10, 20, 30]

h.erase(it2) # Erase 20. 
# it2 is now invalid. it1 stays valid.

print(list(h)) # [10, 30]

h.insert(40) # Might reuse the slot of 20
```
