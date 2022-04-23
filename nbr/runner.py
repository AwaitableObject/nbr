from enum import Enum
from types import TracebackType
from typing import Any, Awaitable, Optional, Type, TypeVar

from httpx import AsyncClient

from nbr.exceptions import SessionExists
from nbr.kernel import Kernel
from nbr.notebook import Notebook
from nbr.schemas.result import RunResult
from nbr.schemas.session import CreateSession, Session
from nbr.utils.client import create_client
from nbr.utils.session import create_session, delete_session, get_sessions

TNotebookRunner = TypeVar("TNotebookRunner", bound="NotebookRunner")


class RunnerState(Enum):
    UNOPENED = 1
    OPENED = 2
    CLOSED = 3


class NotebookRunner:
    def __init__(
        self,
        *,
        notebook: Notebook,
        on_notebook_start: Optional[Awaitable[Any]] = None,
        on_notebook_end: Optional[Awaitable[Any]] = None,
        on_cell_start: Optional[Awaitable[Any]] = None,
        on_cell_end: Optional[Awaitable[Any]] = None,
        host: str = "127.0.0.1",
        port: int = 8888,
        token: Optional[str] = None,
    ) -> None:
        self._state: RunnerState = RunnerState.UNOPENED
        self.token: Optional[str] = token

        self.notebook: Notebook = notebook

        self.host: str = host
        self.port: int = port

        self.on_notebook_start = on_notebook_start
        self.on_notebook_finish = on_notebook_end
        self.on_cell_start = on_cell_start
        self.on_cell_finish = on_cell_end

        self._client: AsyncClient = create_client(
            base_url=f"http://{self.host}:{self.port}/api",
            headers={"Authorization": f"token {self.token}"},
        )

        self._session: Session
        self._kernel: Kernel

    async def execute(self) -> RunResult:
        if self.on_notebook_start:
            await self.on_notebook_start

        run_result = self._kernel.send(data=self.notebook.cells)

        if self.on_notebook_finish:
            await self.on_notebook_finish

        return run_result

    async def __aenter__(self: TNotebookRunner) -> TNotebookRunner:
        if self._state != RunnerState.UNOPENED:
            raise RuntimeError(
                "Cannot open a runner instance more than once.",
            )

        all_sessions = await get_sessions(client=self._client)
        for session in all_sessions:
            if session.name == self.notebook.name:
                raise SessionExists()

        self._state = RunnerState.OPENED
        self._kernel = Kernel()

        self._session = await create_session(
            session_data=CreateSession(
                name=self.notebook.name, path=self.notebook.path
            ),
            client=self._client,
        )

        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        traceback: TracebackType,
    ) -> None:
        await delete_session(session_id=self._session.id, client=self._client)
        self._state = RunnerState.CLOSED
