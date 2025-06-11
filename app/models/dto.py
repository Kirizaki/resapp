from dataclasses import dataclass, field
from typing import List, Optional

# DATA TRANSFER OBJECTS

@dataclass
class ScraperConfig:
    # scraper data
    source: str
    base_url: str

    # offer filters
    city: str
    region: Optional[str] = None
    min_price: Optional[int] = None
    max_price: Optional[int] = None
    min_area: Optional[int] = None
    max_area: Optional[int] = None
    max_price_per_m2: Optional[int] = None
    keywords: List[str] = field(default_factory=list)
    omit_keywords: List[str] = field(default_factory=list)
    allowed_districts: List[str] = field(default_factory=list)
    max_floor: Optional[int] = None
    must_have_garden: bool = False


@dataclass
class OfferRawData:
    html: str
