from httpx import AsyncClient

from nbr.schemas.session import CreateSession, Session


async def create_session(
    host: str, port: int, session: CreateSession, client: AsyncClient
) -> Session:
    """Create a new session."""
    response = await client.post(f"https://{host}:{port}/sessions", json=session.dict())

    return Session(**response.json())


async def delete_session(
    host: str, port: int, session_id: str, client: AsyncClient
) -> None:
    """Delete session by id."""
    url = f"https://{host}:{port}/sessions/{session_id}"

    await client.delete(url)
