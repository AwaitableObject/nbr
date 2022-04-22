from enum import Enum
from types import TracebackType
from typing import Callable, Dict, List, Optional, Type, TypeVar

from httpx import AsyncClient

from nbr.schemas.result import RunResult
from nbr.utils.client import create_client

TNotebookRunner = TypeVar("TNotebookRunner", bound="NotebookRunner")


class RunnerState(Enum):
    UNOPENED = 1
    OPENED = 2
    CLOSED = 3


class NotebookRunner:
    def __init__(
        self,
        *,
        on_notebook_start: Optional[Callable] = None,
        on_notebook_end: Optional[Callable] = None,
        on_cell_start: Optional[Callable] = None,
        on_cell_end: Optional[Callable] = None,
        host: str = "127.0.0.1",
        port: int = 8888,
        token: Optional[str] = None,
    ) -> None:
        self._state: RunnerState = RunnerState.UNOPENED
        self.token = token

        self.host: str = host
        self.port: int = port

        self.on_notebook_start = on_notebook_start
        self.on_notebook_end = on_notebook_end
        self.on_cell_start = on_cell_start
        self.on_cell_end = on_cell_end

        self._client: AsyncClient = create_client(
            base_url=f"http://{self.host}:{self.port}",
            headers={"Authorization": f"token {self.token}"},
        )

    async def execute(self, *, cells: List[Dict]) -> RunResult:
        pass

    async def __aenter__(self: TNotebookRunner) -> TNotebookRunner:
        if self._state != RunnerState.UNOPENED:
            raise RuntimeError(
                "Cannot open a runner instance more than once.",
            )

        self._state = RunnerState.OPENED

        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        traceback: TracebackType,
    ) -> None:
        self._state = RunnerState.CLOSED
