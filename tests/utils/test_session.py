from unittest.mock import AsyncMock, Mock

from nbr.schemas.session import CreateSession, KernelName
from nbr.utils.session import create_session, delete_session, get_sessions
from tests.tools import read_json


async def test__get_sessions() -> None:
    expected_session_data = read_json("session_test.json")

    mocked_response = Mock()
    mocked_response.json.return_value = [expected_session_data]

    mocked_client = AsyncMock()
    mocked_client.get.return_value = mocked_response

    all_sessions = await get_sessions(client=mocked_client)
    assert len(all_sessions) == 1


async def test__create_session() -> None:
    expected_session_data = read_json("session_test.json")

    mocked_response = Mock()
    mocked_response.json.return_value = expected_session_data

    mocked_client = AsyncMock()
    mocked_client.post.return_value = mocked_response

    session_data = CreateSession(
        kernel=KernelName(), name="test_nb.ipynb", path="work/test_nb.ipynb"
    )

    session = await create_session(session_data=session_data, client=mocked_client)

    assert session == expected_session_data


async def test__delete_session() -> None:
    mocked_client = AsyncMock()

    await delete_session(session_id="test_session_id", client=mocked_client)

    mocked_client.delete.assert_awaited_once()
