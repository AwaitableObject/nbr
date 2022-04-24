from enum import Enum
from types import TracebackType
from typing import Any, Awaitable, Optional, Type, TypeVar

from httpx import AsyncClient

from nbr.exceptions import SessionExists
from nbr.kernel import Kernel
from nbr.notebook import Notebook
from nbr.schemas.result import RunResult
from nbr.schemas.session import CreateSession, Session
from nbr.utils.client import create_client, prepare_headers
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
        host: str = "127.0.0.1",
        port: int = 8888,
        token: str = "",
    ) -> None:
        self._state: RunnerState = RunnerState.UNOPENED
        self.token: str = token

        self.notebook: Notebook = notebook

        self.host: str = host
        self.port: int = port

        self.on_notebook_start = on_notebook_start
        self.on_notebook_finish = on_notebook_end

        self._client: AsyncClient = create_client(
            base_url=f"http://{self.host}:{self.port}/api",
            headers=prepare_headers(token),
        )

        self._session: Session
        self._kernel: Kernel

    async def execute_all_cells(self) -> RunResult:
        if self._state != RunnerState.OPENED:
            raise RuntimeError("Create NotebookRunner instance first.")

        if self.on_notebook_start:
            await self.on_notebook_start

        run_result = await self._kernel.execute(cells=self.notebook.cells)

        if self.on_notebook_finish:
            await self.on_notebook_finish

        return run_result

    async def __aenter__(self: TNotebookRunner) -> TNotebookRunner:
        if self._state != RunnerState.UNOPENED:
            raise RuntimeError(
                "Cannot create a NotebookRunner instance more than once.",
            )

        all_sessions = await get_sessions(client=self._client)
        for session in all_sessions:
            if session.name == self.notebook.name and not session.kernel.connections:
                raise SessionExists("Session with same name already exists")

        self._state = RunnerState.OPENED
        self._session = await create_session(
            session_data=CreateSession(
                name=self.notebook.name, path=self.notebook.path
            ),
            client=self._client,
        )
        self._kernel = Kernel(session=self._session)
        await self._kernel.start(base_url=f"{self.host}:{self.port}/api")

        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        traceback: TracebackType,
    ) -> None:
        await delete_session(session_id=self._session.id, client=self._client)

        self._state = RunnerState.CLOSED
