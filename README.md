# 🐍 LaPython

> **The Ultimate C++ STL Port for Python**
>
> *High-performance, memory-optimized, and strict implementation of C++ Standard Template Library containers and algorithms.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

## ⚡ Mission

**LaPython** brings the power, rigor, and distinct behavior of C++ data structures to the Python ecosystem. By leveraging low-level memory optimizations (like `__slots__` and typed arrays) and strict API adherence, we bridge the gap between Python scripts and Systems Engineering concepts.

Whether you need a **doubly-linked list** for O(1) splices, a **vector** with capacity management, or a **red-black tree map**, LaPython has you covered.

---

## 📦 Containers Roadmap

### 🟢 Implemented
| Container | Python Package | Description | Key Features |
|-----------|---------------|-------------|--------------|
| `std::vector` | `cppvector` | Dynamic contiguous array | `reserve`, `capacity`, `shrink_to_fit`, SVO (Small Vector Optimization) |
| `std::list` | `cpplist` | Doubly-linked list | `push_front`, `splice`, `swap`, Stable Iterators |
| `std::forward_list` | `cppforward_list` | Singly-linked list | `push_front`, `insert_after`, Low memory overhead |
| `std::array` | `cpparray` | Fixed-size contiguous array | No overhead, strictly fixed size, `fill`, `swap` |
| `std::deque` | `cppdeque` | Map of fixed-size blocks | **O(1) random access**, O(1) push/pop both ends |
| `std::queue` | `cppqueue` | Container adapter (FIFO) | Wraps any container (Dependency Injection standard) |
| `std::priority_queue` | `cpppriority_queue` | Container adapter (Max Heap) | **Strict MAX Heap** (Python default is Min), `top`, `pop` |
| `std::stack` | `cppstack` | Container adapter (LIFO) | Wraps any container (Dependency Injection standard) |
| `std::bitset` | `cppbitset` | Fixed-size bit array | `&`, `|`, `^` operators, `flip`, `count` |
| `std::map` | `cppmap` | Ordered Associative (Tree) | **Sorted Keys**, `lower_bound`, `upper_bound`, O(log N) |
| `std::set` | `cppset` | Ordered Associative (Tree) | **Sorted Unique Keys**, `lower_bound`, `upper_bound` |
| `std::unordered_map` | `cppunordered_map` | Hash Table (Buckets) | **Separate Chaining**, `load_factor`, `bucket_count` |
| `std::unordered_set` | `cppunordered_set` | Hash Table (Buckets) | **Separate Chaining**, `load_factor`, O(1) avg |

---

## 🧮 Algorithms (Coming Soon)

We are porting the `<algorithm>` header to work generically across all LaPython containers.

### Non-Modifying Sequence Operations
*   `find`, `find_if`, `find_if_not`
*   `count`, `count_if`
*   `mismatch`, `equal`
*   `search`, `search_n`

### Modifying Sequence Operations
*   `copy`, `copy_if`, `copy_n`, `copy_backward`
*   `move`, `move_backward`
*   `fill`, `fill_n`
*   `transform`
*   `generate`, `generate_n`
*   `remove`, `remove_if` (Erase-remove idiom helpers)
*   `unique`
*   `reverse`, `rotate`, `shuffle`

### Sorting & Binary Search
*   `sort` (Introsort hybrid)
*   `stable_sort`
*   `partial_sort`, `nth_element`
*   `lower_bound`, `upper_bound`, `equal_range`, `binary_search`

### Heap Operations
*   `make_heap`, `push_heap`, `pop_heap`, `sort_heap`

### Numeric
*   `iota`, `accumulate`, `inner_product`, `adjacent_difference`, `partial_sum`

---

## 🚀 Installation & Usage

Currently, packages are installed individually from this monorepo.

```bash
# Install Vector
pip install ./cppvector

# Install List
pip install ./cpplist
```

### Example: The "Vector" Experience
```python
from cppvector import Vector

v = Vector()
v.reserve(100) # Pre-allocate memory
v.push_back(42)
print(v.capacity()) # 100
```

### Example: The "List" Experience
```python
from cpplist import List

l1 = List([1, 2, 3])
l2 = List([99, 100])

l1.swap(l2) # O(1) pointer swap
print(l1) # List[2](99, 100)
```

---

## 🤝 Contribution

We welcome strict C++ ports! If you love memory management, distinct data structures, and Python type hints, pull requests are welcome.

**Rules:**
1.  Strict adherence to C++17/20 behavior where possible.
2.  `__slots__` usage for all object-heavy classes.
3.  Full type hinting (`typing.Generic`).

---

*Standard Template Library for the Modern Pythonista.*
