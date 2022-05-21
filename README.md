[![CI](https://github.com/zhivykh/nbr/workflows/CI/badge.svg)](https://github.com/zhivykh/nbr/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/zhivykh/nbr/branch/main/graph/badge.svg?token=8BQOVVCL6B)](https://codecov.io/gh/zhivykh/nbr)
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
from nbr import NotebookRunner, Notebook, JupyterAPI, ExecutionStatus


async def main() -> None:
    jupyter_api = JupyterAPI()
    notebook = Notebook.read_file(path="Untitled.ipynb")

    async with NotebookRunner(notebook=notebook, jupyter_api=jupyter_api) as runner:
        result = await runner.execute_all_cells()

        if result.status == ExecutionStatus.SUCCESS:
            notebook.save(path="Executed.ipynb")
    
if __name__ == "__main__":
    asyncio.run(main())
```