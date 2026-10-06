from __future__ import annotations

from pydantic import BaseModel, Field
from .product import Product
from .search import Requirements


class ComparisonRow(BaseModel):
    feature: str
    values: dict[str, str]


class Recommendation(BaseModel):
    product: Product
    why: str
    labels: list[str] = Field(default_factory=list)


class ChatResponse(BaseModel):
    assistant_message: str
    requirements: Requirements
    products: list[Product] = Field(default_factory=list)
    recommendation: Recommendation | None = None
    comparison: list[ComparisonRow] = Field(default_factory=list)
    awards: dict[str, str] = Field(default_factory=dict)
    evidence_count: int = 0
    disclaimer: str = "AI-generated score based on your requirements and available product evidence."
