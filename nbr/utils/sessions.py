import httpx

from nbr.schemas.session import CreateSession, Session
from nbr.settings import JUPYTER_BASE_URL


async def create_session(session: CreateSession) -> Session:
    """Create a new session."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{JUPYTER_BASE_URL}/sessions", json=session.dict()
        )

    return Session(**response.json())


async def delete_session(session_id: str) -> None:
    url = f"{JUPYTER_BASE_URL}/sessions/{session_id}"
    async with httpx.AsyncClient() as client:
        await client.delete(url)
