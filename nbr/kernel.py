import asyncio
import json
from typing import List

from websockets.legacy.client import WebSocketClientProtocol

from nbr.schemas.message import Content
from nbr.schemas.result import ExecutionStatus, RunResult
from nbr.schemas.session import Session
from nbr.utils.message import create_message
from nbr.utils.websocket import connect_websocket


class Kernel:
    def __init__(self, *, session: Session) -> None:
        self._session: Session = session

        self._websocket: WebSocketClientProtocol
        self._channel_tasks: List[asyncio.Task] = []

        self._status: ExecutionStatus = ExecutionStatus.SUCCESS
        self._cells_count: int

    async def listen_server(self) -> None:
        """Listen server messages."""
        while True:
            msg = await self._websocket.recv()

            msg_json = json.loads(msg)
            content = msg_json["content"]

            if (
                "execution_count" in content
                and content["execution_count"] == self._cells_count
            ):
                self._status = ExecutionStatus.SUCCESS

                await self._stop()
                break

            if "status" in content and content["status"] == "aborted":
                self._status = ExecutionStatus.ERROR

                await self._stop()
                break

    async def start(self, base_url: str) -> None:
        self._websocket = await connect_websocket(base_url=base_url, session=self._session)
        self._channel_tasks.append(asyncio.create_task(self.listen_server()))

    async def _stop(self) -> None:
        self._channel_tasks[-1].cancel()
        await self._websocket.close()

    async def execute(self, cells: List) -> RunResult:

        self._cells_count = len(cells)

        for cell in cells:
            code = cell["source"]

            content = Content(code=code)
            message = create_message(
                channel="shell",
                msg_type="execute_request",
                session=self._session.name,
                content=content,
            )

            await self._websocket.send(message)

        await asyncio.gather(*self._channel_tasks)

        return RunResult(status=self._status)
