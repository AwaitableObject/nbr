from unittest.mock import AsyncMock, patch

import pytest
from httpx import codes
from httpx._models import Response

import nbr.utils.contents as contents_module
from nbr.exceptions import InvalidPathException
from nbr.utils.client import create_client
from tests.tools import read_json


@patch(
    "nbr.utils.contents.get_contents",
    AsyncMock(return_value=read_json("nb_test_folder_contents.json")),
)
async def test__open_directory() -> None:
    client = create_client(base_url="http://localhost:8888", headers={})
    contents = await contents_module.get_contents(path="path_to_folder", client=client)

    assert contents["type"] == "directory"
    assert contents["path"] == "work"


@patch(
    "nbr.utils.contents.get_contents",
    AsyncMock(return_value=read_json("nb_test_contents.json")),
)
async def test__open_notebook() -> None:
    client = create_client(base_url="http://localhost:8888", headers={})
    contents = await contents_module.get_contents(
        path="work/test_nb.ipynb", client=client
    )

    assert contents["type"] == "notebook"
    assert contents["path"] == "work/test_nb.ipynb"


async def test_invalid_path() -> None:
    client = AsyncMock()
    client.get.return_value = Response(status_code=codes.NOT_FOUND)

    with pytest.raises(InvalidPathException):
        await contents_module.get_contents(path="invalid_path", client=client)
