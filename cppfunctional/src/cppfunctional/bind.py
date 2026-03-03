from typing import Any, Callable
import functools

class _Placeholder:
    def __init__(self, index: int):
        self.index = index

_1 = _Placeholder(1)
_2 = _Placeholder(2)
_3 = _Placeholder(3)
_4 = _Placeholder(4)
_5 = _Placeholder(5)
_6 = _Placeholder(6)
_7 = _Placeholder(7)
_8 = _Placeholder(8)
_9 = _Placeholder(9)

def is_placeholder(arg: Any) -> int:
    """Returns the index of the placeholder if it is one, otherwise 0."""
    if isinstance(arg, _Placeholder):
        return arg.index
    return 0

class _BindWrapper:
    def __init__(self, fn: Callable, *bound_args, **bound_kwargs):
        self._fn = fn
        self._bound_args = bound_args
        self._bound_kwargs = bound_kwargs

    def __call__(self, *args, **kwargs):
        # Resolve positional arguments
        resolved_args = []
        for barg in self._bound_args:
            ph_index = is_placeholder(barg)
            if ph_index > 0:
                # Placeholders are 1-indexed
                if ph_index <= len(args):
                    resolved_args.append(args[ph_index - 1])
                else:
                    raise TypeError(f"Missing argument for placeholder _{ph_index}")
            elif isinstance(barg, _BindWrapper):
                resolved_args.append(barg(*args, **kwargs))
            else:
                from .functional import ReferenceWrapper
                if isinstance(barg, ReferenceWrapper):
                    resolved_args.append(barg.get())
                else:
                    resolved_args.append(barg)

        # Resolve keyword arguments
        resolved_kwargs = {}
        for k, v in self._bound_kwargs.items():
            ph_index = is_placeholder(v)
            if ph_index > 0:
                if ph_index <= len(args):
                    resolved_kwargs[k] = args[ph_index - 1]
                else:
                    raise TypeError(f"Missing argument for placeholder _{ph_index} in kwarg {k}")
            elif isinstance(v, _BindWrapper):
                resolved_kwargs[k] = v(*args, **kwargs)
            else:
                from .functional import ReferenceWrapper
                if isinstance(v, ReferenceWrapper):
                    resolved_kwargs[k] = v.get()
                else:
                    resolved_kwargs[k] = v
        
        # Any unused args are ignored by std::bind!
        # Oh, actually, std::bind discards extra args. Wait, no.
        # It's an error if we pass fewer args than required by placeholders,
        # but extra arguments are discarded.
        # Any kwargs passed directly.
        resolved_kwargs.update(kwargs)

        return self._fn(*resolved_args, **resolved_kwargs)

def bind(fn: Callable, *bound_args, **bound_kwargs) -> Callable:
    """
    Simulates std::bind.
    """
    return _BindWrapper(fn, *bound_args, **bound_kwargs)

def bind_front(fn: Callable, *bound_args, **bound_kwargs) -> Callable:
    """
    Simulates std::bind_front.
    """
    return functools.partial(fn, *bound_args, **bound_kwargs)

def bind_back(fn: Callable, *bound_args, **bound_kwargs) -> Callable:
    """
    Simulates std::bind_back.
    """
    def _bind_back_wrapper(*args, **kwargs):
        # First put the runtime positional args, then the bound ones.
        # And mix kwargs.
        combined_kwargs = dict(bound_kwargs)
        combined_kwargs.update(kwargs)
        return fn(*args, *bound_args, **combined_kwargs)
    return _bind_back_wrapper
