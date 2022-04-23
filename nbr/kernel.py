from typing import Dict, List

# from websockets.legacy.client import WebSocketClientProtocol

from nbr.schemas.result import RunResult
from nbr.schemas.session import Session
from nbr.utils.websocket import connect_websocket


class Kernel:
    def __init__(self, *, base_url: str, session: Session) -> None:
        self._session: Session = session
        self._websocket = connect_websocket(
            base_url=base_url, session=self._session
        )

    async def execute(self) -> None:
        pass

    def send(self, data: List[Dict]) -> RunResult:
        pass
