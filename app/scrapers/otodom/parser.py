from app.scrapers.parser_base import BaseParser


class OtodomScraper(BaseParser):
    def __init__(self):
        super().__init__()

    def build_listing_url(self, page: int) -> str:
        return (
            f"{self._config['base_url']}/pl/wyniki/sprzedaz/mieszkanie/{self._config['region']}/{self._config['city']}"
            f"?viewType=listing&page={page}&by=LATEST&direction=DESC"
            )

    def build_offer_url(self, offer_url: str):
        return f"{self._config['base_url']}{offer_url}"
