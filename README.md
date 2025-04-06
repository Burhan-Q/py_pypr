# Py-Pypr

Py-Pypr is a pure Python library for functional shift operators, enabling readable  and intuitive multi-step data transformation pipelines.

## Features

- Chainable pipelines for data transformation.

- Functional programming style with decorators.

- Lightweight and easy to use.

## Installation

To install Py-Pypr, use `pip` or `uv`:

```bash
uv pip install "git+https://github.com/Burhan-Q/py_pypr/"
```

```bash
pip install "git+https://github.com/Burhan-Q/py_pypr/"
```

## Usage

### Basic Example

```python
from py_pypr import PypObject, Pypline


# Create a PypObject
data = PypObject("  hello world  ")

# pipelines
strip_pipeline = Pypline(str.strip)
uppercase_pipeline = Pypline(str.upper)

# Chain pipelines
data >> strip_pipeline >> uppercase_pipeline

# Get the result
print(data.result())  # Output: "HELLO WORLD"
```


### Using the `pypr` Decorator

```python
from py_pypr import PypObject, pypr


@pypr
def replace_spaces(data: str) -> str:
    return data.replace(" ", "_")

# Create a PypObject
data = PypObject("hello world")

# Apply the decorated function
data >> replace_spaces

# Get the result
print(data.result())  # Output: "hello_world"
```

### Advanced Example

```python
import numpy as np
from py_pypr import PypObject, Pypline, pypr

stepwise = True
# Define object
arr = PypObject(np.ones((3, 120, 120)))

# Establish transforms
def add_to_upperleft(np_arr: np.ndarray, val: int | float) -> np.ndarray:
    y, x = np.array(np_arr.shape[1:]) // 2
    return np_arr[:, :y, :x] + val  # return is required

@pypr(val=12)
def mul_righthalf(np_arr: np.ndarray, val: int | float) -> np.ndarray:
    x = np.array(np_arr.shape[2:]) // 2
    np_arr[:, :, x.item():] *= val
    return np_arr

# Create Pypline
add_5_top_left = Pypline(add_to_upperleft, 5)

if stepwise:
    # Transform iteratively
    arr.data.mean()  # start value (1.0)

    for pyp in (add_5_top_left, mul_righthalf):
        _ = arr >> pyp
        arr.data.mean()  # new value (6.0; 39.0)
else:
    # Transform single line
    arr >> add_5_top_left >> mul_righthalf
    arr.data.mean()  # new value (39.0)
```


## Documentation

For detailed documentation, visit the [GitHub repository](https://github.com/Burhan-Q/py_pypr).


## License

Py-Pypr is licensed under the BSD 3-Clause License. See the [LICENSE](LICENSE) file for details.


