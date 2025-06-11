from bs4 import BeautifulSoup

from app.scrapers.models.dto import ScraperConfig
from app.utils.logger import Logger

logger = Logger().get_logger()


class BaseParser:
    def __init__(self, config: ScraperConfig):
        self._config = config

    def extract_surface(self, text: str) -> int:
        try:
            return int(float(text.split()[0].replace(",", ".")))
        except Exception:
            return 0

    def extract_floor(self, text: str) -> int:
        if "parter" in text.lower():
            return 0
        try:
            return int(text.lower().split(" ")[0])
        except Exception:
            return 99

    def extract_price(self, text: str) -> int:
        try:
            return int(text.replace(" ", "").replace("zł", "").replace(",", "").strip())
        except Exception:
            return 0

    def _any_keywords_in_text(self, text: str, keywords: list[str]):
        return any(word.lower() in text for word in keywords)

    def _safe_extract_text_by_attributes(self, element: str, attributes: dict, soup: BeautifulSoup) -> str:
        text = ''
        try:
            text = soup.find(element, attrs=attributes).text.strip()
        except Exception as e:
            logger.error("Could not get text", extra={"element": element, "attributes": attributes, 'soup': soup})

        return text