import asyncio
import json
from typing import Coroutine, List, Optional

from httpx import AsyncClient
from websockets.legacy.client import WebSocketClientProtocol

from nbr.schemas.message import Content
from nbr.schemas.session import CreateSession, Session
from nbr.utils.client import create_client
from nbr.utils.message import connect_websocket, create_message
from nbr.utils.sessions import create_session, delete_session


class KernelDriver:
    """Kernel driver class."""

    def __init__(self) -> None:
        """Init then kernel driver."""
        self.session: Session
        self._cells_count: int

        self._websocket: WebSocketClientProtocol
        self._client: AsyncClient = create_client()

        self._channel_tasks: List[asyncio.Task] = []
        self._callback: Optional[Coroutine]

    def set_callback(self, callback: Optional[Coroutine]) -> None:
        """Set callback."""
        self._callback = callback

    async def listen_server(self) -> None:
        """Listen server messages."""
        while True:
            msg = await self._websocket.recv()

            msg_json = json.loads(msg)
            content = msg_json["content"]
            channel = msg_json["channel"]

            if channel == "iopub" and msg_json["msg_type"] in [
                "error",
                "execute_result",
                "execute_input",
                "stream",
            ]:
                print(content)

            if "execution_count" in content:
                if content["execution_count"] == self._cells_count:
                    await self.stop()
                    break

            if "status" in content and content["status"] == "aborted":
                await self.stop()
                break

    async def start(self, session_name: str) -> None:
        """Run a kernel."""
        self.session = await create_session(
            session=CreateSession(name=session_name), client=self._client
        )
        self._websocket = await connect_websocket(self.session)

        self._channel_tasks.append(asyncio.create_task(self.listen_server()))

    async def stop(self) -> None:
        """Stop a kernel."""
        self._channel_tasks[-1].cancel()

        if self._callback:
            await self._callback

        await self._websocket.close()
        await delete_session(session_id=self.session.id, client=self._client)

    async def execute(self, cells: List) -> None:
        """Execute the cell."""

        self._cells_count = len(cells)

        for cell in cells:
            code = cell["source"]

            content = Content(code=code)
            message = create_message(
                channel="shell",
                msg_type="execute_request",
                session=self.session.name,
                content=content,
            )

            await self._websocket.send(message)
