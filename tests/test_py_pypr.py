import re
import pytest

from py_pypr.core import PypObject, Pypline
from py_pypr.decos import pypr


def test_pypobject_init() -> None:
    """Tests the initialization of the `PypObject` class."""
    obj = PypObject("test_data")
    assert obj.data == "test_data"
    assert obj.pos == 0
    assert obj.kw == ""


def test_pypobject_rshift() -> None:
    """Tests the right shift operator (`>>`) for chaining pipelines."""
    obj = PypObject(" test_data ")
    pipeline = Pypline(str.strip)
    obj >> pipeline
    assert obj.data == "test_data"
    obj = PypObject(" test_data ")
    obj >>= pipeline
    assert obj == "test_data"


def test_pypobject_result() -> None:
    """Tests the `result` method of the `PypObject` class."""
    obj = PypObject("test_data")
    assert obj.result() == "test_data"


def test_pypobject_pos() -> None:
    """Tests the `pos` attribute of the `PypObject` class."""
    rgx: re.Pattern[str] = re.compile(r"(data)")
    obj = PypObject("test_data", pos=1)
    obj >> Pypline(rgx.sub, "pypr")
    assert obj == "test_pypr"


def test_pypobject_kw() -> None:
    """Tests the `kw` attribute of the `PypObject` class."""

    def do_thing(a, keyword: str = "this"):
        return list(keyword)

    obj = PypObject("test_data", kw="keyword")
    pypl = Pypline(do_thing, 2)
    obj >> pypl
    assert obj == ["t", "e", "s", "t", "_", "d", "a", "t", "a"]


def test_pypobject_repr() -> None:
    """Tests the string representation of the `PypObject` class."""
    obj = PypObject("test_data")
    assert repr(obj) == "PypObject(data=test_data)"


def test_pyobject_type_error() -> None:
    """Tests the `TypeError` when trying to chain with a non-callable object."""
    with pytest.raises(TypeError):
        PypObject(123) >> "this will fail"


def test_pypline_initialization() -> None:
    """Tests the initialization of the `Pypline` class."""
    pipeline = Pypline(str.upper)
    assert pipeline.func == str.upper


def test_pypline_call() -> None:
    """Tests the call method of the `Pypline` class."""
    obj = PypObject("test_data")
    pipeline = Pypline(str.upper)
    obj >> pipeline
    assert obj.data == "TEST_DATA"
    assert (obj >> Pypline(str.lower)).result() == "test_data"


def test_pypline_type_error() -> None:
    """Tests the `TypeError` when trying to apply a `Pypline` to a non-`PypObject`."""
    with pytest.raises(TypeError):
        Pypline(str.strip)("this will fail")


def test_pypline_repr() -> None:
    """Tests the string representation of the `Pypline` class."""
    pipeline = Pypline(str.upper)
    assert repr(pipeline) == "Pypline(func=upper, args=(), kwargs={})"


def test_pypline_args_kwargs() -> None:
    """Tests the handling of arguments and keyword arguments in the `Pypline` class."""

    def zipper(a, b, strict=False) -> list:
        return list(zip(a, b, strict=strict))

    obj = PypObject([1, 2, 3, 4])
    pipeline = Pypline(zipper, ("a", "b", "c", "d"), strict=True)
    assert pipeline.func == zipper
    assert pipeline.args == (("a", "b", "c", "d"),)
    assert pipeline.kwargs == {"strict": True}
    obj >> pipeline
    assert obj.data == [(1, "a"), (2, "b"), (3, "c"), (4, "d")]


@pytest.mark.parametrize(
    "data, swap, expected",
    [
        ("test_data", None, "test-data"),
        ("test_data", "-", "test-data"),
        ("another_test", "+++", "another+++test"),
        ("_pypline_", "|", "|pypline|"),
    ],
)
def test_pypr_decorator(data, swap, expected) -> None:
    """Tests the `pypr` decorator with different inputs."""
    if swap:

        @pypr(val=swap)
        def un_snake(str_in: str, val: str = "-") -> str:
            return str_in.replace("_", val)
    else:

        @pypr
        def un_snake(str_in: str, val: str = "-") -> str:
            return str_in.replace("_", val)

    obj = PypObject(data)
    obj >> un_snake
    assert obj.data == expected
