from pydantic import BaseModel
class Review(BaseModel):
    id: int
    productId: int
    userId: int
    rating: float
    comment: str | None