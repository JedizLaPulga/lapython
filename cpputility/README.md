# cpputility

> **C++ Vocabulary Types for Python**

Implementations of standard C++ utility types: `std::pair`, `std::optional`, `std::variant`, and strict tuples.

## Features
*   **Pair**: Strictly typed pair `Pair[T1, T2]` with `.first` and `.second`.
*   **Optional**: Null-safe wrapper `Optional[T]` ensuring explicit value access.
*   **Variant**: Type-safe union `Variant[T1, T2, ...]` (simplified).

## usage

```python
from cpputility import Pair, Optional

p = Pair(1, "Hello")
print(p.first)  # 1
print(p.second) # "Hello"

opt = Optional.make(42)
if opt.has_value():
    print(opt.value()) # 42
```
