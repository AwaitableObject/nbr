from nbr.schemas.session import Session
from nbr.utils.websocket import connect_websocket
from tests.tools import read_json


async def test__connect() -> None:
    session_data = read_json("session_test.json")
    session = Session(**session_data)
    connection = connect_websocket(base_url="base_url", session=session)

    expected = (
        "ws://base_url/kernels/test_kerkel_id/channels?session_id=test_session_id"
    )

    assert connection._uri == expected  # pylint: disable=W0212
