from pydantic import BaseModel
from typing import List, Optional


class Product(BaseModel):
    product_name: str
    concentration: Optional[str]
    skin_type: List[str]
    key_ingredients: List[str]
    benefits: List[str]
    how_to_use: Optional[str]
    side_effects: Optional[str]
    price: Optional[int]


class FAQItem(BaseModel):
    question: str
    answer: str


class FAQList(BaseModel):
    question_list: List[FAQItem]

class FAQOutput(BaseModel):
    product: str
    faqs: FAQList


class QuestionList(BaseModel):
    questions: List[str]


class ProductPage(BaseModel):
    product_name: str
    summary: str
    benefits: List[str]
    skin_types: List[str]
    key_ingredients: List[str]
    how_to_use: str
    side_effects: str
    price: int


class ComparisonPage(BaseModel):
    product_a_name: str
    product_b_name: str
    similarities: List[str]
    differences: List[str]
    recommended_for_product_a: str
    recommended_for_product_b: str
    summary: str
