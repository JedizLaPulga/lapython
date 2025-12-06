# cppmap

A C++ style `std::map<K, V>` implementation (Ordered Associative Container).

## Difference vs `dict`
| Feature | `std::map` (`cppmap`) | `dict` (Python) |
|---------|-----------------------|-----------------|
| **Ordering** | **Sorted by Key** value | Insertion Order |
| **Structure**| Tree (BST/RB) | Hash Table |
| **Search Ops**| `lower_bound`, `upper_bound` | N/A |
| **Complexity**| O(log N) | O(1) |

## Usage
```python
from cppmap import Map

m = Map()
m[10] = "Ten"
m[1] = "One"
m[5] = "Five"

# Iteration is ALWAYS sorted by key: 1, 5, 10
for k, v in m.items():
    print(k, v)

# Range searches
print(m.lower_bound(4)) # 5 (First key >= 4)
print(m.upper_bound(5)) # 10 (First key > 5)
```
