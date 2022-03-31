from httpx import AsyncClient


def create_client() -> AsyncClient:
    """Create AsyncClient."""
    return AsyncClient()
