from enum import Enum
from types import TracebackType
from typing import Callable, Optional, Type, TypeVar

from nbr.schemas.result import RunResult

TNotebookRunner = TypeVar("TNotebookRunner", bound="NotebookRunner")


class RunnerState(Enum):
    UNOPENED = 1
    OPENED = 2
    CLOSED = 3


class NotebookRunner:
    host: str
    port: int

    def __init__(
        self,
        *,
        on_notebook_start: Optional[Callable] = None,
        on_notebook_end: Optional[Callable] = None,
        on_cell_start: Optional[Callable] = None,
        on_cell_end: Optional[Callable] = None,
        host: str = "127.0.0.1",
        port=8888,
    ) -> None:
        self._state: RunnerState = RunnerState.UNOPENED
        self.host: str = host
        self.port: int = port

    async def execute(self, *, cells: list[dict]) -> RunResult:
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
        exc_type: Type[BaseException] = None,
        exc_value: BaseException = None,
        traceback: TracebackType = None,
    ) -> None:
        self._state = RunnerState.CLOSED
