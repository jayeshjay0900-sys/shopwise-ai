from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class SearchQuery(BaseModel):
    """User's search query"""
    query: str = Field(..., min_length=1, description="Natural language shopping query")


class Requirement(BaseModel):
    """Extracted requirements from user query"""
    category: Optional[str] = None
    brand: Optional[str] = None
    model_family: Optional[str] = None
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    must_have_features: List[str] = Field(default_factory=list)
    use_case: Optional[str] = None
    comparison_mode: bool = False
    comparison_products: List[str] = Field(default_factory=list)


class ProductEvidence(BaseModel):
    """Product evidence from a single source"""
    name: str
    price: Optional[float] = None
    currency: str = "INR"
    url: str
    source: str
    specifications: Dict[str, Any] = Field(default_factory=dict)
    description: Optional[str] = None


class ReviewSentiment(BaseModel):
    """Review sentiment analysis"""
    positive_percentage: Optional[float] = None
    negative_percentage: Optional[float] = None
    neutral_percentage: Optional[float] = None
    summary: str = "Review sentiment unavailable"
    available: bool = False


class Product(BaseModel):
    """Final product recommendation"""
    name: str
    price: Optional[float] = None
    currency: str = "INR"
    url: str
    source: str
    image_url: Optional[str] = None
    specifications: Dict[str, Any] = Field(default_factory=dict)
    pros: List[str] = Field(default_factory=list)
    cons: List[str] = Field(default_factory=list)
    match_score: float = Field(ge=0, le=100)
    review_sentiment: ReviewSentiment = Field(default_factory=ReviewSentiment)
    evidence_urls: List[str] = Field(default_factory=list)


class SearchResponse(BaseModel):
    """Complete search response"""
    query: str
    requirements: Requirement
    products: List[Product]
    recommendation: str
    comparison_mode: bool = False
    error: Optional[str] = None
