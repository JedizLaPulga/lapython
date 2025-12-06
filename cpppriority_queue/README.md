# cpppriority_queue

A C++ style `std::priority_queue` implementation.

## ⚠️ Important Difference vs `heapq`
Standard Python `heapq` implements a **Min Heap** (smallest element is popped first).
C++ `std::priority_queue` implements a **Max Heap** (largest element is popped first).

**`cpppriority_queue` strictly follows C++ semantics: It is a MAX HEAP.**

## Usage

```python
from cpppriority_queue import PriorityQueue

pq = PriorityQueue()

# Elements are ordered by their comparison operators (>)
pq.push(10)
pq.push(30)
pq.push(5)

print(pq.top()) # 30 (Largest)
pq.pop()

print(pq.top()) # 10
```

## Features
- **Max Heap**: No need to negate numbers hack. Default behavior is Max.
- **Strict API**: `push`, `pop`, `top`, `empty`, `size`.
- **Pure Python**: Implemented with custom sift-up/sift-down logic for transparency and correctness without relying on potentially confusing negation wrappers around `heapq`.
