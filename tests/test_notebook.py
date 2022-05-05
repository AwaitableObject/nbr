import os
from unittest.mock import AsyncMock, patch

import nbformat

from nbr.notebook import Notebook
from tests.tools import read_json

CWD = os.path.dirname(__file__)


def test__notebook_read_file() -> None:
    notebook_name = "test_nb.ipynb"
    path = f"{CWD}/notebooks/{notebook_name}"
    nb = Notebook.read_file(path=path)

    assert nb.name == notebook_name
    assert nb.path == path
    assert nb.is_remote is False
    assert len(nb.cells) == 1


@patch(
    "nbr.notebook.get_contents",
    AsyncMock(return_value=read_json("nb_test_contents.json")),
)
async def test__notebook_read_remote() -> None:
    notebook_name = "test_nb.ipynb"
    path = f"work/{notebook_name}"

    nb = await Notebook.read_remote(path=path)

    assert nb.name == notebook_name
    assert nb.path == path
    assert nb.is_remote is True
    assert len(nb.cells) == 1


def test__notebook_content() -> None:
    notebook_name = "test_nb.ipynb"
    path = f"{CWD}/notebooks/{notebook_name}"
    nb = Notebook.read_file(path=path)

    nb_nbformat = nbformat.read(path, as_version=4)

    assert nb.dict() == nb_nbformat


def test__notebook_save() -> None:
    notebook_name = "test_nb.ipynb"
    path = f"{CWD}/notebooks/{notebook_name}"
    path_of_copy = f"{CWD}/notebooks/copy_{notebook_name}"

    nb = Notebook.read_file(path=path)
    nb.save(path=path_of_copy)

    assert os.path.exists(path_of_copy) is True
