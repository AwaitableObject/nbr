from enum import Enum
from types import TracebackType
from typing import Any, Awaitable, Dict, List, Optional, Type, TypeVar

from httpx import AsyncClient

from nbr.kernel import Kernel
from nbr.schemas.session import CreateSession, Session
from nbr.utils.client import create_client
from nbr.utils.session import create_session, delete_session

TNotebookRunner = TypeVar("TNotebookRunner", bound="NotebookRunner")


class RunnerState(Enum):
    UNOPENED = 1
    OPENED = 2
    CLOSED = 3


class NotebookRunner:
    def __init__(
        self,
        *,
        on_notebook_start: Optional[Awaitable[Any]] = None,
        on_notebook_end: Optional[Awaitable[Any]] = None,
        on_cell_start: Optional[Awaitable[Any]] = None,
        on_cell_end: Optional[Awaitable[Any]] = None,
        host: str = "127.0.0.1",
        port: int = 8888,
        token: Optional[str] = None,
    ) -> None:
        self._state: RunnerState = RunnerState.UNOPENED
        self.token = token

        self.host: str = host
        self.port: int = port

        self.on_notebook_start = on_notebook_start
        self.on_notebook_finish = on_notebook_end
        self.on_cell_start = on_cell_start
        self.on_cell_finish = on_cell_end

        self._client: AsyncClient = create_client(
            base_url=f"http://{self.host}:{self.port}",
            headers={"Authorization": f"token {self.token}"},
        )

        self._session: Session
        self._kernel: Kernel

    async def execute(self, *, cells: List[Dict]) -> None:
        if self.on_notebook_start:
            await self.on_notebook_start

        for cell in cells:
            self._kernel.send(data=cell["source"])

        if self.on_notebook_finish:
            await self.on_notebook_finish

    async def __aenter__(self: TNotebookRunner) -> TNotebookRunner:
        if self._state != RunnerState.UNOPENED:
            raise RuntimeError(
                "Cannot open a runner instance more than once.",
            )

        self._state = RunnerState.OPENED

        self._kernel = Kernel()
        self._session = await create_session(
            session_data=CreateSession(name="aboba"), client=self._client
        )

        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        traceback: TracebackType,
    ) -> None:

        await delete_session(session_id=self._session.name, client=self._client)

        self._state = RunnerState.CLOSED
