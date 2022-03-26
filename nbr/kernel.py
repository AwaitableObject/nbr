import json
from typing import Dict, Optional, Union
from uuid import uuid4

import httpx
from websockets.legacy.client import WebSocketClientProtocol, connect

from nbr.schemas.message import Content, Header, Message, Metadata
from nbr.schemas.session import CreateSession, Session
from nbr.settings import JUPYTER_BASE_URL, JUPYTER_WS_URL


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
    content: Optional[Union[Content, dict]] = None,
    metadata: Optional[Union[Metadata, dict]] = None,
) -> Dict:
    """Generate a message using a template."""
    if content is None:
        content = {}

    if metadata is None:
        metadata = {}

    header = Header(msg_type=message_type, session=session)

    message_data = {
        "buffers": [],
        "channel": channel,
        "header": header,
        "content": content,
        "metadata": metadata,
        "parent_header": {},
    }

    message = Message(**message_data)
    print(message.dict())

    return message.dict()


class KernelDriver:
    """Kernel driver class."""

    def __init__(self, session_name: str, session_type: str = "notebook") -> None:
        """Init then kernel driver."""
        self.kernel_name = "python3"

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
            channel="shell",
            message_type="kernel_info_request",
            session=self.session.id,
            content=Content(),
            metadata=Metadata(),
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

        message = create_message(
            channel="shell",
            message_type="execute_request",
            session=self.session.id,
            content=Content(code=code),
            metadata=Metadata(),
        )

        message_json = json.dumps(message)
        await self.websocket.send(message_json)
        for _ in range(2):
            msg = await self.websocket.recv()
            print(msg)
