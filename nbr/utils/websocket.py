from websockets.legacy.client import Connect, connect

from nbr.schemas.session import Session


def connect_websocket(session: Session) -> Connect:
    """Connect to websocket."""

    kernel_id = session.kernel.id
    session_id = session.id
    url = f"/kernels/{kernel_id}/channels?session_id={session_id}"

    return connect(url)
