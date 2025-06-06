import asyncio
from abc import ABC, abstractmethod
from typing import List, Dict
from urllib.parse import urlparse, parse_qs
import httpx
from bs4 import BeautifulSoup
from models.scraper_config import ScraperConfig
from scrapers.engines.base_engine import BaseEngine

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


class BaseScraper(ABC):
    def __init__(self, engine: BaseEngine, config: ScraperConfig):
        self.engine = engine
        self.config = config
        self.src = None

    @abstractmethod
    async def build_listing_url(self, page: int) -> str:
        pass

    @abstractmethod
    def extract_offer_details(self, soup: BeautifulSoup, url: str) -> Dict:
        pass

    @abstractmethod
    def should_include_offer(self, offer: Dict) -> bool:
        pass

    @abstractmethod
    def build_offer_url(self, city, page):
        pass

    async def scrape(self) -> List[Dict]:
        offers = []
        page_urls = await self.fetch_page_urls()

        for page_url in page_urls:
            listing_urls = await self.fetch_listing_links_from_page(page_url)
            tasks = [self.fetch_and_parse_offer(url) for url in listing_urls]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            for offer in results:
                if isinstance(offer, dict) and self.should_include_offer(offer):
                    offers.append(offer)

            await asyncio.sleep(1)

        return offers

    async def fetch_page_urls(self) -> List[str]:
        urls = []
        page = 1
        last_page = None

        async with httpx.AsyncClient(timeout=10) as client:
            while True:
                url = await self.build_listing_url(page)
                res = await client.get(url, headers=HEADERS)
                current_page = self._get_page_number_from_url(res.url)

                if current_page is None or current_page == last_page:
                    break

                last_page = current_page
                urls.append(url)
                page += 1
                await asyncio.sleep(0.5)

        return urls

    async def fetch_listing_links_from_page(self, page_url: str) -> List[str]:
        soup = await self.engine.fetch(page_url)
        articles = soup.find_all("article", attrs={"data-cy": "listing-item"})
        self.build_offer_url(city=self.city)
        return [
            "https://www.otodom.pl" + a.find("a")["href"].split("?")[0]
            for a in articles if a.find("a")
        ]

    async def fetch_and_parse_offer(self, url: str) -> Dict:
        try:
            soup = await self.engine.fetch(url)
            return self.extract_offer_details(soup, url)
        except Exception as e:
            print(f"[{self.src}] Error parsing {url}: {e}")
            return {}

    def _get_page_number_from_url(self, url: str) -> int:
        parsed_url = urlparse(str(url))
        page_number = parse_qs(parsed_url.query).get('page', [None])[0]
        return int(page_number) if page_number else None
