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
    notebook = Notebook(name="Untitled.ipynb", path="work/Untitled.ipynb")

    async with NotebookRunner(
        notebook=notebook,
        host="127.0.0.1",
        port=8888,
        token="a30acc5051c2f2687df3a839f9962d797f074691f9597923",
    ) as runner:
        await runner.execute()


if __name__ == "__main__":
    asyncio.run(main())
```