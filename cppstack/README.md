# cppstack

A C++ style `std::stack` (LIFO) adapter implementation.

## Usage

```python
from cppstack import Stack
# Optional: Use with strict containers via dependency injection
# from cppvector import Vector

# 1. Default (uses internal list fallback)
s = Stack() 
s.push(1)
s.push(2)
print(s.top())   # 2
s.pop()          # Removes 2 (Strictly, C++ pop returns void, but we allow side-effect free removal)
                 # Note: Implementation calls pop_back on container.

# 2. Dependency Injection
# s = Stack(container=Vector()) 
```

## API
*   `push(x)`: Inserts at top.
*   `pop()`: Removes from top.
*   `top()`: Returns top element.
*   `empty()`: Returns boolean.
*   `size()`: Returns count.
