# cppqueue

A C++ style `std::queue` adapter implementation.

In C++, `queue` is not a container itself, but a **container adapter**. It wraps an underlying sequential container (usually `deque` or `list`) and restricts interfaces to `push`, `pop`, `front`, and `back`.

## Usage

```python
from cppqueue import Queue
# Optional: Use with strict containers like cppdeque via dependency injection
# from cppdeque import Deque 

# 1. Default (uses internal list fallback if no container provided)
q = Queue() 
q.push(1)
q.push(2)
print(q.front()) # 1
q.pop()          # Removes 1

# 2. Dependency Injection (The "Real" C++ way)
# q = Queue(container=Deque()) 
```

## API
*   `push(x)`: Inserts at back.
*   `pop()`: Removes from front.
*   `front()`: Returns first element.
*   `back()`: Returns last element.
*   `empty()`: Returns boolean.
*   `size()`: Returns count.
