class Vector:
    """A simple implementation of a dynamic array similar to C++ std::vector"""
    
    def __init__(self, capacity=8):
        self._capacity = capacity
        self._size = 0
        self._data = [None] * capacity

    def size(self):
        return self._size

    def capacity(self):
        return self._capacity

    def empty(self):
        return self._size == 0

    def push_back(self, value):
        if self._size == self._capacity:
            self._resize(self._capacity * 2)
        self._data[self._size] = value
        self._size += 1

    def pop_back(self):
        if self._size == 0:
            raise IndexError("pop_back() on empty vector")
        self._size -= 1
        value = self._data[self._size]
        self._data[self._size] = None  # optional: help GC
        # Optional shrink (like shrink_to_fit)
        if self._size > 0 and self._size == self._capacity // 4:
            self._resize(self._capacity // 2)
        return value

    def _resize(self, new_capacity):
        if new_capacity < self._size:
            new_capacity = self._size
        new_data = [None] * new_capacity
        for i in range(self._size):
            new_data[i] = self._data[i]
        self._data = new_data
        self._capacity = new_capacity

    def __getitem__(self, index):
        if index < 0:
            index += self._size
        if index < 0 or index >= self._size:
            raise IndexError("vector index out of range")
        return self._data[index]

    def __setitem__(self, index, value):
        if index < 0:
            index += self._size
        if index < 0 or index >= self._size:
            raise IndexError("vector assignment index out of range")
        self._data[index] = value

    def clear(self):
        self._size = 0
        # Optional: keep capacity or reset to initial
        # self._capacity = 8
        # self._data = [None] * self._capacity

    def __len__(self):
        return self._size

    def __repr__(self):
        return f"Vector({self._data[:self._size]})"

    def __iter__(self):
        for i in range(self._size):
            yield self._data[i]