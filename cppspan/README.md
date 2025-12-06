# cppspan

A Python implementation of C++ `std::span`.

`std::span` is a non-owning view over a contiguous sequence of objects.

## Usage

```python
from cppspan import Span

data = [1, 2, 3, 4, 5]
s = Span(data)
print(s.front())  # 1
print(s.back())   # 5

sub = s.subspan(1, 3) # view over [2, 3, 4]
sub[0] = 99
print(data) # [1, 99, 3, 4, 5] - modifying span modifies source!
```
