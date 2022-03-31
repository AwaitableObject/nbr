from typing import Any, Coroutine, Dict, List, Optional

from nbr.kernel import KernelDriver
from nbr.utils.client import create_client
from nbr.utils.contents import get_contents


class JupyterNotebook:
    """JupyterNotebook class."""

    def __init__(self, name: str) -> None:
        """Init notebook."""
        self.name = name
        self.cells: List[dict] = []
        self._kernel_driver = KernelDriver()
        self._content: Dict[str, Any] = {}
        self._client = create_client()

    @property
    async def content(self) -> dict:
        """Return contents of notebook."""
        return self._content

    async def open(self) -> None:
        """Open the notebook."""
        notebook_contents = await get_contents(
            path=f"work/{self.name}", client=self._client
        )
        self._content = notebook_contents["content"]
        self.cells = self._content["cells"]

        await self._kernel_driver.start(session_name=self.name)

    async def run_all_cells(self, callback: Optional[Coroutine] = None) -> None:
        """Run all cells."""
        self._kernel_driver.set_callback(callback)

        await self._kernel_driver.execute(self.cells)

    def __str__(self) -> str:
        return f"<Notebook {self.name}>"

    def __repr__(self) -> str:
        return f"<Notebook {self.name}>"
