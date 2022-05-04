import os

from nbr.notebook import Notebook


def test__notebook_creation() -> None:
    notebook_name = "test_nb.ipynb"
    path = f"{os.getcwd()}/tests/notebooks/{notebook_name}"

    nb = Notebook.read_file(path=path)

    assert nb.name == notebook_name
