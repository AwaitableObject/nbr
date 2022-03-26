import asyncio
import json
from datetime import datetime, timezone
from typing import Dict, List, Optional
from uuid import uuid4

import httpx
from websockets.legacy.client import WebSocketClientProtocol, connect

from nbrunner.schemas import CreateSession, Session
from nbrunner.settings import JUPYTER_BASE_URL, JUPYTER_WS_URL

executed = []

async def create_session(session: CreateSession) -> Session:
    """Create a new session."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{JUPYTER_BASE_URL}/sessions", json=session.dict()
        )

    return Session(**response.json())


def create_message(
    channel: str,
    message_type: str,
    session: str,
    content: Optional[dict] = None,
    metadata: Optional[dict] = None,
) -> Dict:
    """Generate a message using a template."""
    if content is None:
        content = {}

    if metadata is None:
        metadata = {}

    message = {
        "buffers": [],
        "channel": channel,
        "content": content,
        "header": {
            "date": str(datetime.utcnow().replace(tzinfo=timezone.utc)),
            "msg_id": uuid4().hex,
            "msg_type": message_type,
            "session": session,
            "username": "",
            "version": "5.2",
        },
        "metadata": metadata,
        "parent_header": {},
    }
    return message


class KernelDriver:
    """Kernel driver class."""

    def __init__(self, session_name: str, cells, session_type: str = "notebook") -> None:
        """Init then kernel driver."""
        self.kernel_name = "python3"
        self.cells = cells

        self.session: Session
        self.websocket: WebSocketClientProtocol
        self.session_name = session_name
        self.session_path = uuid4().hex
        self.session_type = session_type

    async def start(self) -> None:
        """Run a kernel."""
        session_json = {
            "kernel": {"name": self.kernel_name},
            "name": str(self.session_name),
            "path": self.session_path,
            "type": self.session_type,
        }

        self.session = await create_session(CreateSession(**session_json))
        await self.create_kernel_channel()     
        
        for _ in range(5):
            await self.websocket.recv()

    async def create_kernel_channel(self) -> None:
        """Create new kernel channel."""
        kernel_id = self.session.kernel.id
        session_id = self.session.id
        url = f"{JUPYTER_WS_URL}/kernels/{kernel_id}/channels?session_id={session_id}"

        message = create_message(
            channel="shell", message_type="kernel_info_request", session=self.session.id
        )

        self.websocket = await connect(url)
        await self.websocket.send(json.dumps(message))
        await self.websocket.recv()

    async def stop(self) -> None:
        """Stop a kernel."""
        await self.websocket.close()

        url = f"{JUPYTER_BASE_URL}/sessions/{self.session.id}"
        async with httpx.AsyncClient() as client:
            await client.delete(url)

    async def execute(self, cell: dict) -> None:
        """Execute the cell."""

        code = cell["source"]

        content = {
            "allow_stdin": False,
            "code": code,
            "silent": False,
            "stop_on_error": True,
            "store_history": True,
            "user_expressions": {},
        }
        metadata = {
            "cellId": uuid4().hex,
            "deletedCells": [],
            "recordTiming": False,
        }
        message = create_message(
            channel="shell",
            message_type="execute_request",
            session=self.session.id,
            content=content,
            metadata=metadata,
        )

        message_json = json.dumps(message)
        await self.websocket.send(message_json)
        for _ in range(2):
            msg = await self.websocket.recv()
            print(msg)
        
