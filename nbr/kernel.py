import json
from typing import Dict, Optional, Union

from websockets.legacy.client import WebSocketClientProtocol, connect

from nbr.schemas.message import Content, Header, Message, Metadata
from nbr.schemas.session import CreateSession, Session
from nbr.settings import JUPYTER_WS_URL
from nbr.utils.sessions import create_session, delete_session


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
        "channel": channel,
        "header": header,
        "content": content,
        "metadata": metadata,
    }

    message = Message(**message_data)

    return message.dict()


class KernelDriver:
    """Kernel driver class."""

    def __init__(self, session_name: str) -> None:
        """Init then kernel driver."""
        self._running = False
        self._websocket: WebSocketClientProtocol
        self.session: Session

        self.session_name = session_name

    @property
    def running(self) -> bool:
        return self._running

    async def start(self) -> None:
        """Run a kernel."""
        self.session = await create_session(CreateSession(name=self.session_name))
        await self.create_kernel_channel()

        self._running = True

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

        self._websocket = await connect(url)
        await self._websocket.send(json.dumps(message))
        await self._websocket.recv()

    async def stop(self) -> None:
        """Stop a kernel."""
        await self._websocket.close()
        await delete_session(self.session.id)

        self._running = False

    async def execute(self, cell: dict) -> None:
        """Execute the cell."""
