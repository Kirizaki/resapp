from typing import Protocol


class DataProcessor(Protocol):
    def __init__(self, nextProcessor: DataProcessor)
    async def process(self, data) -> None:
        ...