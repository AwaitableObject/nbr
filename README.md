# nbr
NBR lets you **run** remote jupyter-notebooks.

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

Run a notebook on this server:


```python
import asyncio
from nbr import JupyterNotebook

async def main() -> None:
    nb = JupyterNotebook("Untitled.ipynb")
    
    await nb.open()
    await nb.run_all_cells()
    await nb.close()
    
if __name__ == "__main__":
    asyncio.run(main())
```