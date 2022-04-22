from httpx import AsyncClient

from nbr.schemas.session import CreateSession, Session


async def create_session(session: CreateSession, client: AsyncClient) -> Session:
    """Create a new session."""
    response = await client.post("/sessions", json=session.dict())

    return Session(**response.json())


async def delete_session(session_id: str, client: AsyncClient) -> None:
    """Delete session by id."""
    url = f"/sessions/{session_id}"

    await client.delete(url)
