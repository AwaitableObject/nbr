from typing import Dict, List

from nbr.api import JupyterAPI
from nbr.exceptions import NBFormatModuleNotFound
from nbr.utils.client import create_client, prepare_headers
from nbr.utils.contents import get_contents


class Notebook:
    def __init__(self, *, name: str, path: str) -> None:
        self.name = name
        self.path = path
        self.cells: List[Dict] = []

        self._remote: bool = False

    def save(self, path: str) -> None:
        if not self._remote:
            try:
                import nbformat
            except ImportError as exc:
                raise NBFormatModuleNotFound("nbformat module required") from exc

            nbformat.write(self.dict(), path)

    @classmethod
    async def read_remote(
        cls, path: str, jupyter_api: JupyterAPI = JupyterAPI()
    ) -> "Notebook":
        client = create_client(
            base_url=f"http://{jupyter_api.host}:{jupyter_api.host}/api",
            headers=prepare_headers(jupyter_api.token),
        )
        notebook_name = path.split("/")[-1]
        notebook = cls(name=notebook_name, path=path)

        nb_content = await get_contents(path=path, client=client)
        notebook.cells = nb_content["content"]["cells"]

        notebook._remote = True

        return notebook

    @classmethod
    def read_file(cls, path: str) -> "Notebook":
        try:
            import nbformat
        except ImportError as exc:
            raise NBFormatModuleNotFound("nbformat module required") from exc

        nb_file = nbformat.read(path, as_version=4)
        notebook_name = path.split("/")[-1]

        notebook = cls(name=notebook_name, path=path)
        notebook.cells = nb_file.cells

        return notebook

    def dict(self) -> Dict:
        return {
            "cells": self.cells,
            "metadata": {"language_info": {"name": "python"}},
            "nbformat": 4,
            "nbformat_minor": 2,
        }
