import json

from nbr.utils.message import create_message


def test__create_base_message() -> None:
    message = create_message(
        channel="test_channel", msg_type="test_msg_type", session="test_session"
    )

    assert isinstance(message, str) is True

    json_msg = json.loads(message)

    assert json_msg["channel"] == "test_channel"
    assert json_msg["header"]["msg_type"] == "test_msg_type"
    assert json_msg["header"]["session"] == "test_session"
