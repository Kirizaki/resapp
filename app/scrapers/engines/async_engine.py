import httpx
from bs4 import BeautifulSoup
from scrapers.engines.base_engine import BaseEngine


class AsyncEngine(BaseEngine):
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=10)

    async def fetch(self, url: str):
        res = await self.client.get(url, headers={"User-Agent": "Mozilla/5.0"})
        return BeautifulSoup(res.text, "html.parser")
