from typing import Optional, Union

from websockets.legacy.client import Connect, connect

from nbr.config import config
from nbr.schemas.message import Content, Header, Message, Metadata
from nbr.schemas.session import Session


def create_message(
    channel: str,
    msg_type: str,
    session: str,
    content: Optional[Union[Content, dict]] = None,
    metadata: Optional[Union[Metadata, dict]] = None,
) -> str:
    """Generate a message using a template."""
    if not content:
        content = {}

    if not metadata:
        metadata = {}

    header = Header(msg_type=msg_type, session=session)

    message_data = {
        "channel": channel,
        "header": header,
        "content": content,
        "metadata": metadata,
    }

    message = Message(**message_data)

    return message.json()


def connect_websocket(session: Session) -> Connect:
    """Connect to websocket."""

    kernel_id = session.kernel.id
    session_id = session.id
    url = f"{config.ws_url}/kernels/{kernel_id}/channels?session_id={session_id}"

    return connect(url)
