from factories.config_factory import ScraperConfigFactory
from scrapers.otodom_scraper import OtodomScraper
from scrapers.engines.async_engine import AsyncEngine

config = ScraperConfigFactory.from_json("configs/wrzeszcz_config.json")
scraper = OtodomScraper(engine=AsyncEngine(), config=config)