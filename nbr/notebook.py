from typing import Any, Dict, List

from nbr.contents import get_contents
from nbr.kernel import KernelDriver


class JupyterNotebook:
    """JupyterNotebook class."""

    def __init__(self, name: str) -> None:
        """Init notebook."""
        self.name = name
        self.cells: List[dict] = []
        self.kernel_driver = KernelDriver(session_name=self.name)
        self._content: Dict[str, Any] = {}

    async def open(self) -> None:
        """Open the notebook."""
        notebook_contents = await get_contents(f"/work/{self.name}")
        self._content = notebook_contents["content"]
        self.cells = self._content["cells"]

        await self.kernel_driver.start()

    async def run_all_cells(self) -> None:
        """Run all cells."""
        for cell in self.cells:
            res = await self.kernel_driver.execute(cell)
            print(res)

    async def close(self) -> None:
        """Close kernel."""
        await self.kernel_driver.stop()
