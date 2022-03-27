from typing import Dict

import httpx

from nbr.config import config


async def get_contents(path: str) -> Dict:
    """Get content by path."""
    url = f"{config.api_url}/contents{path}"
    print(url)

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()
