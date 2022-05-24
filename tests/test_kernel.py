# type: ignore
from unittest.mock import AsyncMock, patch

from nbformat import NotebookNode

from nbr.kernel import Kernel
from nbr.schemas.result import ExecutionStatus
from nbr.schemas.session import Session
from tests.tools import read_json


def test__kernel_creation() -> None:
    session_data = read_json("session_test.json")
    session = Session(**session_data)

    kernel = Kernel(session=session)

    assert kernel._status == ExecutionStatus.WAITING
    assert len(kernel._channel_tasks) == 0


@patch("nbr.kernel.connect_websocket", AsyncMock())
async def test__kernel_start() -> None:
    session_data = read_json("session_test.json")
    session = Session(**session_data)
    base_url = "ws://test_base_url"

    kernel = Kernel(session=session)
    kernel.listen_server = AsyncMock()

    await kernel.start(base_url=base_url)

    assert len(kernel._channel_tasks) == 1


@patch("nbr.kernel.connect_websocket", AsyncMock())
async def test__kernel_start_and_stop() -> None:
    session_data = read_json("session_test.json")
    session = Session(**session_data)
    base_url = "ws://test_base_url"

    kernel = Kernel(session=session)
    kernel.listen_server = AsyncMock()
    kernel._websocket = AsyncMock()

    await kernel.start(base_url=base_url)
    await kernel._stop()


@patch("nbr.kernel.connect_websocket", AsyncMock())
async def test__kernel_execute() -> None:
    session_data = read_json("session_test.json")
    session = Session(**session_data)
    base_url = "ws://test_base_url"
    kernel = Kernel(session=session)
    kernel.listen_server = AsyncMock()
    await kernel.start(base_url=base_url)

    result = await kernel.execute(cells=[])
    assert len(result.cells) == 0

    kernel._status = ExecutionStatus.SUCCESS
    result = await kernel.execute(cells=[NotebookNode({"source": "2 + 2"})])
    assert result.status == ExecutionStatus.SUCCESS
    assert len(result.cells) == 1
