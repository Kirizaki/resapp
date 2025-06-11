from abc import ABC, abstractmethod
from urllib.parse import urlparse, parse_qs
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

from app.scrapers.models.dto import ScraperConfig, OfferRawData


class BaseScraper(ABC):
    def __init__(self, config: ScraperConfig):
        self._config = config
        self._source = self._config['source']
        self._current_page = 0
        self._loaded_page = self._current_page

    async def scrape(self):
        offers = []
        async with async_playwright() as p:
            # browser = await p.chromium.launch(headless=True)
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()

            while self._is_end() == False:
                listing_url = self.build_listing_url(self._current_page)
                await page.goto(listing_url)

                if self._current_page > 0 and not self._update_loaded_page_number(page.url):
                    self._current_page += 1
                    continue

                content = BeautifulSoup(await page.content(), "html.parser")
                for article in content.find_all("a", attrs={"data-cy": "listing-item-link"}):
                    await page.goto(self.build_offer_url(article.get('href')))
                    offers.append(OfferRawData(html=await page.content()))

            await browser.close()
        return offers

    def _update_loaded_page_number(self, url: str):
        try:
            self._loaded_page = self._get_loaded_page_number(url)
        except Exception as e:
            print(f"Error on getting loaded page number: {e}")
            return False

    def _get_loaded_page_number(self, url):
        parsed = urlparse(url)
        query = parse_qs(parsed.query)

        return int(query.get("page", [None])[0]) if "page" in query else None

    def _is_end(self):
        return self._loaded_page < self._current_page

    @abstractmethod
    def build_listing_url(self, page: int) -> str:
        pass

    @abstractmethod
    def build_offer_url(self, city, page):
        pass
