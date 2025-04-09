from __future__ import annotations

from typing import Callable


class PypObject:
    """
    A class to represent a data object that can be processed through a pipeline.

    It allows chaining of functions to transform the data step by step.

    Attributes:
        data (Any): The data to be processed.
        pos (int): The position for the data in the function arguments, default is 0.
        kw (str): The keyword argument for data to be used in the function, default is ''.

    Example:
        ```python
        txt = PypObject("this is text.  ")
        p1 = Pypline(str.strip)
        p2 = Pypline(str.replace, " ", "_")
        p3 = Pypline(str.title)
        (txt >> p1 >> p2 >> p3).result()
        # Output: This_Is_Text.
        ```
    """

    def __init__(self, data: object, pos: int = 0, kw: str = "") -> None:
        self.data: object = data
        self._data: object = data
        self.pos: int = pos
        self.kw: str = kw

    def __rshift__(self, pipeline: "Pypline") -> "PypObject":
        """Chain the pipeline with the current data."""
        if not callable(pipeline):
            raise TypeError("Cannot chain with non-callable object")
        self.data = pipeline(self)
        return self

    def result(self) -> object:
        """Return the final result of the pipeline."""
        return self.data

    def __repr__(self) -> str:
        """Return a string representation of the PypObject."""
        return f"PypObject(data={self.data})"

    def __eq__(self, other) -> bool:
        return self.data == (other.data if isinstance(other, PypObject) else other)


class Pypline:
    """
    A class to represent a pipeline step that can be applied to a PypObject.

    Attributes:
        func (Callable): The function to be applied in the pipeline.
        args (tuple): The arguments to be passed to the function.
        kwargs (dict): The keyword arguments to be passed to the function.

    Example:
        ```python
        p1 = Pypline(str.strip)
        p2 = Pypline(str.replace, " ", "_")
        p3 = Pypline(str.title)
        txt = PypObject("this is text.  ")
        (txt >> p1 >> p2 >> p3).result()
        # Output: This_Is_Text.
        ```
    """

    def __init__(self, func: Callable, *args, **kwargs) -> None:
        self.func: Callable = func
        self.args: tuple = args
        self.kwargs: dict = kwargs

    def __call__(self, pyp_obj: PypObject) -> PypObject:
        """Execute the pipeline step on the provided PypObject."""
        if not (isinstance(pyp_obj, PypObject) or issubclass(type(pyp_obj), PypObject)):
            raise TypeError("Pypline can only be applied to PypObject")
        kwargs: dict = self.kwargs | {pyp_obj.kw: pyp_obj.data} if pyp_obj.kw else self.kwargs

        args = list(self.args)
        if pyp_obj.pos:
            args.insert(pyp_obj.pos, pyp_obj.data)
        elif pyp_obj.kw not in kwargs:
            args.insert(0, pyp_obj.data)

        return self.func(*args, **kwargs)

    def __repr__(self) -> str:
        return f"Pypline(func={self.func.__name__}, args={self.args}, kwargs={self.kwargs})"
