from app.processors.processor_base import DataProcessor
from app.processors.db_processor import DbProcessor

class ResultsProcessor(DataProcessor):
    def __init__(self, nextProcessor: DbProcessor):
        self.nextProcessor = nextProcessor

    async def process(self, data):
        print(f"[DB_proc] processing: {data}")
