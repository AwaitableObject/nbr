[![CI](https://github.com/zhivykh/nbr/workflows/CI/badge.svg)](https://github.com/zhivykh/nbr/actions/workflows/main.yml) [![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/) [![Stable Version](https://img.shields.io/pypi/v/nbr?color=blue)](https://pypi.org/project/nbr/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

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

from nbr import JupyterAPI, Notebook, NotebookRunner


async def main() -> None:
    jupyter_api = JupyterAPI(token="481145d4be3c79620c23e2bb4e5b818a3669c4e88ea75c35")
    notebook = await Notebook.read_remote(
        path="work/Untitled.ipynb", jupyter_api=jupyter_api
    )

    async with NotebookRunner(notebook=notebook, jupyter_api=jupyter_api) as runner:
        result = await runner.execute_all_cells()
        print(result.status)


if __name__ == "__main__":
    asyncio.run(main())
```