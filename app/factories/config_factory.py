import json
from pathlib import Path
from models.scraper_config import ScraperConfig

class ScraperConfigFactory:
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