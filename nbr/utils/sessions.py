import httpx

from nbr.config import config
from nbr.schemas.session import CreateSession, Session


async def create_session(session: CreateSession) -> Session:
    """Create a new session."""
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{config.api_url}/sessions", json=session.dict())

    return Session(**response.json())


async def delete_session(session_id: str) -> None:
    url = f"{config.api_url}/sessions/{session_id}"
    async with httpx.AsyncClient() as client:
        await client.delete(url)
