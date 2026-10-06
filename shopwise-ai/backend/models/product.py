from __future__ import annotations

from typing import Any
from urllib.parse import urlparse
from pydantic import BaseModel, Field, field_validator


def _http_url(value: str) -> str:
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("URL must be a valid HTTP URL")
    return value


class PricePoint(BaseModel):
    retailer: str
    amount: float | None = Field(default=None, ge=0)
    currency: str = "INR"
    url: str | None = None

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: str | None) -> str | None:
        return _http_url(value) if value else value


class Sentiment(BaseModel):
    positive: int = Field(ge=0, le=100)
    neutral: int = Field(ge=0, le=100)
    negative: int = Field(ge=0, le=100)

    @field_validator("negative")
    @classmethod
    def total_is_reasonable(cls, value: int, info: Any) -> int:
        data = info.data
        if value + data.get("positive", 0) + data.get("neutral", 0) > 100:
            raise ValueError("sentiment percentages cannot exceed 100")
        return value


class Evidence(BaseModel):
    title: str
    url: str
    source_type: str = "web"
    snippet: str = ""

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: str) -> str:
        return _http_url(value)


class Product(BaseModel):
    name: str
    brand: str = "Not available"
    category: str = "Not available"
    product_type: str = "Not available"
    price: float | None = Field(default=None, ge=0)
    currency: str = "INR"
    rating: float | None = Field(default=None, ge=0, le=5)
    review_count: int | None = Field(default=None, ge=0)
    image_url: str | None = None
    specifications: dict[str, str] = Field(default_factory=dict)
    pros: list[str] = Field(default_factory=list)
    cons: list[str] = Field(default_factory=list)
    review_summary: str = "Not available"
    sentiment: Sentiment | None = None
    match_score: int = Field(default=0, ge=0, le=100)
    score_explanation: str = "Not available"
    product_url: str | None = None
    review_urls: list[str] = Field(default_factory=list)
    source_urls: list[str] = Field(default_factory=list)
    prices: list[PricePoint] = Field(default_factory=list)
    evidence: list[Evidence] = Field(default_factory=list)

    @field_validator("product_url")
    @classmethod
    def validate_product_url(cls, value: str | None) -> str | None:
        return _http_url(value) if value else value

    @field_validator("image_url")
    @classmethod
    def validate_image_url(cls, value: str | None) -> str | None:
        return _http_url(value) if value else value

    @field_validator("review_urls", "source_urls")
    @classmethod
    def validate_link_lists(cls, values: list[str]) -> list[str]:
        return [_http_url(value) for value in values]


class ResearchResult(BaseModel):
    title: str
    url: str
    content: str = ""
    score: float | None = None
    purpose: str = "web"
    image_url: str | None = None

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: str) -> str:
        return _http_url(value)

    @field_validator("image_url")
    @classmethod
    def validate_image_url(cls, value: str | None) -> str | None:
        return _http_url(value) if value else value


class ProductExtraction(BaseModel):
    price: float | None = Field(default=None, ge=0)
    rating: float | None = Field(default=None, ge=0, le=5)
    review_count: int | None = Field(default=None, ge=0)
    specifications: dict[str, str] = Field(default_factory=dict)
    pros: list[str] = Field(default_factory=list)
    cons: list[str] = Field(default_factory=list)
    review_summary: str = "Not available"


class ReviewAnalysis(BaseModel):
    pros: list[str] = Field(default_factory=list)
    cons: list[str] = Field(default_factory=list)
    summary: str = "Not available"
    sentiment: Sentiment
    review_urls: list[str] = Field(default_factory=list)

    @field_validator("review_urls")
    @classmethod
    def validate_review_urls(cls, values: list[str]) -> list[str]:
        return [_http_url(value) for value in values]
