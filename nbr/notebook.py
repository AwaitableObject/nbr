from typing import Any, Dict, List

from nbr.contents import get_contents
from nbr.kernel import KernelDriver


class JupyterNotebook:
    """JupyterNotebook class."""

    def __init__(self, name: str) -> None:
        """Init notebook."""
        self.name = name
        self.cells: List[dict] = []
        self._kernel_driver = KernelDriver(session_name=self.name)
        self._content: Dict[str, Any] = {}

    @property
    async def content(self) -> dict:
        if not self._content:
            await self.open()

        return self._content

    async def open(self) -> None:
        """Open the notebook."""
        notebook_contents = await get_contents(f"/work/{self.name}")
        self._content = notebook_contents["content"]
        self.cells = self._content["cells"]

    async def run_all_cells(self) -> None:
        """Run all cells."""

        if not self._kernel_driver.running:
            self._kernel_driver.start()

        for cell in self.cells:
            res = await self._kernel_driver.execute(cell)
            print(res)

    async def close(self) -> None:
        """Close kernel."""
        await self._kernel_driver.stop()

    def __str__(self) -> str:
        return f"<Notebook {self.name}>"

    def __repr__(self) -> str:
        return f"<Notebook {self.name}>"
