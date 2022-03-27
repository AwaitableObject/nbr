from typing import Dict

import httpx

from nbr.config import Config


async def get_contents(path: str) -> Dict:
    """Get content by path."""
    url = f"{Config.api_url}/contents{path}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()
