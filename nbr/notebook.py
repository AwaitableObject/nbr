from typing import Dict, List

from nbr.exceptions import NBFormatModuleNotFound
from nbr.utils.client import create_client, prepare_headers
from nbr.utils.contents import get_contents


class Notebook:
    def __init__(self, *, name: str, path: str) -> None:
        self.name = name
        self.path = path
        self.cells: List[Dict] = []

    @classmethod
    async def read_remote(
        cls,
        path: str,
        host: str = "127.0.0.1",
        port: int = 8888,
        token: str = "",
    ) -> "Notebook":
        client = create_client(
            base_url=f"http://{host}:{port}/api",
            headers=prepare_headers(token),
        )
        notebook_name = path.split("/")[-1]
        notebook = cls(name=notebook_name, path=path)

        nb_content = await get_contents(path=path, client=client)
        notebook.cells = nb_content["content"]["cells"]

        return notebook

    @classmethod
    def read_file(cls, file_name: str) -> "Notebook":
        try:
            import nbformat
        except ImportError as exc:
            raise NBFormatModuleNotFound("nbformat module required") from exc

        nb_file = nbformat.read(file_name, as_version=4)

        notebook = cls(name=file_name, path=f"work/{file_name}")
        notebook.cells = nb_file.cells

        return notebook

    def dict(self) -> Dict:
        return {
            "cells": self.cells,
            "metadata": {"language_info": {"name": "python"}},
            "nbformat": 4,
            "nbformat_minor": 2,
        }
