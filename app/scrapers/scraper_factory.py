import json
from pathlib import Path
from app.scrapers.otodom.scraper import OtodomScraper
from app.scrapers.models.dto import ScraperConfig
from app.utils.logger import Logger

logger = Logger().get_logger()

class ScraperFactory:
    """Factory for creating scraper instances based on source name."""

    _scrapers = {
        "otodom": OtodomScraper,
    }

    @staticmethod
    def create(site: str, config: dict):
        site = site.lower()

        if site not in ScraperFactory._scrapers:
            logger.error("Unsupported scraper requested", extra={"site": site})
            raise ValueError(f"Unsupported site: {site}")

        logger.debug("Creating scraper instance", extra={"site": site, "config": config})
        return ScraperFactory._scrapers[site](config=config)
    
    @staticmethod
    def from_json(file_path: str) -> ScraperConfig:
        config_data = json.loads(Path(file_path).read_text())
        return ScraperConfig(**config_data)

    @staticmethod
    def default_for_gdansk_wrzeszcz() -> ScraperConfig:
        return ScraperConfig(
            city="gdansk",
            region="pomorskie",
            min_area=40,
            max_area=80,
            max_floor=0,
            max_price_per_m2=12000,
            allowed_districts=["wrzeszcz", "oliwa"],
            keywords=["ogród", "balkon"],
            omit_keywords=["kamienica", "do remontu"],
            must_have_garden=True,
        )

    @staticmethod
    def from_dict(data: dict) -> ScraperConfig:
        return ScraperConfig(**data)