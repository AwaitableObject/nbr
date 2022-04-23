from typing import Any, Dict

from httpx import AsyncClient


def create_client(base_url: str, headers: Dict[Any, Any]) -> AsyncClient:
    """Create AsyncClient."""
    return AsyncClient(base_url=base_url, headers=headers)
