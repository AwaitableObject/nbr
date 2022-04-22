[![CI](https://github.com/zhivykh/nbr/workflows/CI/badge.svg)](https://github.com/zhivykh/nbr/actions/workflows/main.yml)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

# nbr
NBR lets you **run** local and remote jupyter-notebooks.

## Installation
In a terminal, run:
```
python3 -m pip install nbr
```

## Usage

Launch a Jupyter server:
```
jupyter server --ServerApp.token='' --ServerApp.password='' --ServerApp.disable_check_xsrf=True
```

Execution a local notebook, using a remote server:


```python
import nbr
import nbformat
import asyncio

async def main() -> None:
    nb_file = nbformat.read("Untitled.ipynb", as_version=4)
    
    async with nbr.NotebookRunner(host="127.0.0.1", port=8888) as runner:
        result = await runner.execute(cells=nb_file.cells)
        
        nb_file.cells = result.executed_cells
        nbformat.write(nb_file, "executed_notebook.ipynb")
    
if __name__ == "__main__":
    asyncio.run(main())
```