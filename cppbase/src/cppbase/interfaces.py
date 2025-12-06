class Container:
    """Base interface for all C++ Style Containers."""
    __slots__ = ()
    pass

class Sequence(Container):
    """Base for Sequence containers (vector, list, array, deque, forward_list)."""
    __slots__ = ()
    pass

class Associative(Container):
    """Base for Associative containers (map, set)."""
    __slots__ = ()
    pass

class Unordered(Container):
    """Base for Unordered containers (unordered_map, unordered_set)."""
    __slots__ = ()
    pass

class Adapter(Container):
    """Base for Container Adapters (stack, queue, priority_queue)."""
    __slots__ = ()
    pass
