from __future__ import annotations

from typing import Callable

from .core import Pypline


def pypr(f=None, /, **d_kwargs) -> Pypline | Callable[[Callable], Pypline]:
    """
    A decorator to create a Pypline instance from a function. Augments can be passed as keyword arguments.

    Args:
        d_kwargs: Keyword arguments to be passed to the Pypline.

    Returns:
        Callable: A decorator function that wraps a callable into a Pypline instance.
    """

    def decorator(func: Callable) -> Pypline:
        return Pypline(func=func, **d_kwargs)

    return decorator(func=f) if f else decorator
