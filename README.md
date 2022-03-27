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

Execute a notebook through that server:

```
nbr --server http://127.0.0.1:8888 --run work/Untitled.ipynb
```