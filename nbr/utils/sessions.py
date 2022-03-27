import httpx

from nbr.schemas.session import CreateSession, Session
from nbr.config import Config


async def create_session(session: CreateSession) -> Session:
    """Create a new session."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{Config.api_url}/sessions", json=session.dict()
        )

    return Session(**response.json())


async def delete_session(session_id: str) -> None:
    url = f"{Config.api_url}/sessions/{session_id}"
    async with httpx.AsyncClient() as client:
        await client.delete(url)
