from pydantic import BaseModel
from .review import Review

class Product(BaseModel):
    id: str
    name: str
    price: float
    category: str
    description: str | None = None
    reviews: list[Review] | None = None
