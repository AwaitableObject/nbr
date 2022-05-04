import os
from unittest.mock import AsyncMock, patch

from nbr.notebook import Notebook
from tests.utils import read_json


def test__notebook_read_file() -> None:
    notebook_name = "test_nb.ipynb"
    path = f"{os.getcwd()}/tests/notebooks/{notebook_name}"

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
