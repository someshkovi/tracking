from dataclasses import dataclass
from typing import Optional


@dataclass
class ProductSearchResult:
    name: str
    price: Optional[int]
    rating: Optional[float]
    url: Optional[str]
    reviews_count: Optional[int]
    ratings_count: Optional[int]
    specification: Optional[list]
