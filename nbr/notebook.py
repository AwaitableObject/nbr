from typing import Dict, List


class Notebook:
    def __init__(self, *, name: str, path: str) -> None:
        self.name = name
        self.path = path

        self.cells: List[Dict] = []

    async def open(self) -> None:
        pass

    def dict(self) -> List[Dict]:
        return self.cells
