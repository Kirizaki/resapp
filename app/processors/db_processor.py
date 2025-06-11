from app.processors.processor_base import DataProcessor
from app.db.offer_repository import OfferRepository

class DbProcessor(DataProcessor):
    def __init__(self, repo: OfferRepository):
        self._repo = repo

    async def process(self, data):
        print(f"[DB_proc] processing: {data}")
