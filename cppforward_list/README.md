# cppforward_list

A C++ style `std::forward_list` (singly linked list) implementation.

## Comparison vs `cpplist`
| Feature | `forward_list` | `list` |
|---------|---------------|--------|
| **Structure** | Singly Linked | Doubly Linked |
| **Overhead** | 1 pointer/node (lighter) | 2 pointers/node |
| **Iterators** | Forward only | Bidirectional |
| **Ops** | `push_front` only | `push_front`, `push_back` |
| **Insert** | `insert_after` | `insert` |

## Usage
```python
from cppforward_list import ForwardList

fl = ForwardList([1, 2, 3])
fl.push_front(0)
# List is now: 0 -> 1 -> 2 -> 3

# Insert '99' after the first element
it = fl.begin() # points to 0
fl.insert_after(it, 99)
# List: 0 -> 99 -> 1 -> 2 -> 3
```

Ideal for hash map collisions chains or when simple sequencing is needed with minimal memory overhead.
