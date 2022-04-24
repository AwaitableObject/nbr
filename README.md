[![CI](https://github.com/zhivykh/nbr/workflows/CI/badge.svg)](https://github.com/zhivykh/nbr/actions/workflows/main.yml)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![Stable Version](https://img.shields.io/pypi/v/nbr?color=blue)](https://pypi.org/project/nbr/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

# nbr
NBR lets you **run** local and remote jupyter-notebooks.

## Installation
In a terminal, run:
```
pip install nbr
```

## Usage

Launch a Jupyter server:
```
jupyter server
```

Execution a local notebook, using a remote server:


```python
import asyncio
from nbr import NotebookRunner, Notebook


async def main() -> None:
    notebook = Notebook.read_file(name="Untitled.ipynb")

    async with NotebookRunner(
        notebook=notebook,
        host="127.0.0.1",
        port=8888,
        token="481145d4be3c79620c23e2bb4e5b818a3669c4e88ea75c35",
    ) as runner:
        result = await runner.execute_all_cells()
        print(result.status)


if __name__ == "__main__":
    asyncio.run(main())
```