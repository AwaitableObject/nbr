from typing import Dict

import httpx

from nbrunner.settings import JUPYTER_BASE_URL


async def get_contents(path: str) -> Dict:
    """Get content by path."""
    url = f"{JUPYTER_BASE_URL}/contents{path}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()
