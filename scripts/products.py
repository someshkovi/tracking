from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Product:
    name: Optional[str] = field(default=None)
    price: Optional[int] = field(default=None)
    rating: Optional[float] = field(default=None)
    url: Optional[str] = field(default=None)
    site: Optional[str] = field(default=None)
    reviews_count: Optional[int] = field(default=None)
    ratings_count: Optional[int] = field(default=None)
    availability: bool = field(default=False)
    availability_message: Optional[str] = field(default=None)
    specifications: Optional[list] = field(default=None)


@dataclass
class ProductSearchResult:
    name: str
    price: Optional[int]
    rating: Optional[float]
    url: Optional[str]
    reviews_count: Optional[int]
    ratings_count: Optional[int]
    specification: Optional[list]
