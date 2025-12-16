from pydantic import BaseModel

class InventorySummary(BaseModel):
    id: str
    name: str
    location: str
    products: dict[str, int] | None = None
    categories: list[str] | None = None

class ProductSummary(BaseModel):
    id: str
    name: str
    price: float
    category: str
    count: int

class Inventory(BaseModel):
    id: str
    name: str
    location: str
    products: dict[str, int] | None = None