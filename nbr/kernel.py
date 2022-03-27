from websockets.legacy.client import WebSocketClientProtocol, connect

from nbr.config import config
from nbr.schemas.message import Content
from nbr.schemas.session import CreateSession, Session
from nbr.utils.messages import create_message
from nbr.utils.sessions import create_session, delete_session


class KernelDriver:
    """Kernel driver class."""

    def __init__(self) -> None:
        """Init then kernel driver."""
        self._running = False
        self._websocket: WebSocketClientProtocol
        self.session: Session

    @property
    def running(self) -> bool:
        return self._running

    async def start(self, session_name: str) -> None:
        """Run a kernel."""
        self.session = await create_session(CreateSession(name=session_name))
        await self.create_kernel_channel()

        self._running = True

    async def create_kernel_channel(self) -> None:
        """Create new kernel channel."""
        kernel_id = self.session.kernel.id
        session_id = self.session.id
        url = f"{config.ws_url}/kernels/{kernel_id}/channels?session_id={session_id}"

        self._websocket = await connect(url)

    async def stop(self) -> None:
        """Stop a kernel."""
        await self._websocket.close()
        await delete_session(self.session.id)

        self._running = False

    async def execute(self, cell: dict) -> None:
        """Execute the cell."""
        code = cell["source"]

        content = Content(code=code)
        message = create_message(
            channel="shell",
            msg_type="execute_request",
            session=self.session.name,
            content=content,
        )

        await self._websocket.send(message)
        for _ in range(4):
            await self._websocket.recv()
