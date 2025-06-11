import asyncio
from app.processors.processor_base import DataProcessor
from app.scrapers.scraper_base import BaseScraper


class ScraperRunner:
    def __init__(self, scrapers: list[BaseScraper], processor: DataProcessor) -> None:
        self._scrapers = scrapers
        self._processor = processor

    async def run(self) -> None:
        async def run_scraper(scraper):
            offers = await scraper.scrape()
            await self._processor.process(offers)

        await asyncio.gather(*(run_scraper(scraper) for scraper in self._scrapers))
