from pydantic import BaseModel
from typing import List


class Product(BaseModel):
    product_name: str
    concentration: str
    skin_type: List[str]
    key_ingredients: List[str]
    benefits: List[str]
    how_to_use: str
    side_effects: str
    price: int


class FictionalProduct(BaseModel):
    product_name: str
    key_ingredients: List[str]
    benefits: List[str]
    price: int
