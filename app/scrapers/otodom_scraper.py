from bs4 import BeautifulSoup
from models.scraper_config import ScraperConfig
from scrapers.base_scraper import BaseScraper
from scrapers.engines.base_engine import BaseEngine
from utils.offer_filters import filter_offer
from utils.parsers import extract_offer_details
from utils.csv_writer import save_offer_backup

BASE_URL = "https://www.otodom.pl"

###
# config = ScraperConfig(
#     city="gdansk",
#     min_area=40,
#     max_area=90,
#     max_floor=0,
#     max_price_per_m2=12000,
#     keywords=["ogród", "balkon"],
#     omit_keywords=["kamienica", "do remontu"],
#     allowed_districts=["wrzeszcz", "oliwa"],
#     must_have_garden=True,
# )

# scraper = OtodomScraper(engine=AsyncEngine(), config=config)
###
class OtodomScraper(BaseScraper):
    def __init__(self, engine: BaseEngine, config: ScraperConfig):
        super().__init__(engine, config)
        self.config.source = 'otodom'

    async def build_listing_url(self, page: int) -> str:
        return (
            f"{BASE_URL}/pl/wyniki/sprzedaz/mieszkanie/pomorskie/gdansk"
            f"?viewType=listing&page={page}&by=LATEST&direction=DESC"
        )

    def extract_offer_details(self, soup: BeautifulSoup, url: str):
        offer = extract_offer_details(soup, url, self.src)
        save_offer_backup(offer, f"{self.src}.csv")
        return offer

    def should_include_offer(self, offer: dict) -> bool:
        return filter_offer(offer, self)

    def build_offer_url(self, city, page):
        return f"{BASE_URL}/pl/wyniki/sprzedaz/mieszkanie/{city}?page={page}"