from abc import ABC, abstractmethod
from typing import Any


class BaseEngine(ABC):
    @abstractmethod
    async def fetch(self, url: str) -> Any:
        """Fetch the page and return raw HTML or parsed object"""
        pass
