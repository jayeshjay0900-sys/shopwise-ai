from __future__ import annotations

from pydantic import BaseModel, Field


class Requirements(BaseModel):
    category: str = "Not available"
    product_type: str = "Not available"
    brand: str = "Not available"
    model_family: str = "Not available"
    budget: float | None = Field(default=None, ge=0)
    currency: str = "INR"
    use_case: str = "Not available"
    use_cases: list[str] = Field(default_factory=list)
    priority: str = "Not available"
    must_have: list[str] = Field(default_factory=list)
    preferences: list[str] = Field(default_factory=list)
    exclusions: list[str] = Field(default_factory=list)
    comparison_targets: list[str] = Field(default_factory=list)
    raw_query: str


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    conversation_id: str = Field(min_length=1, max_length=120)
    message: str = Field(min_length=1, max_length=2000)
    context: list[ChatMessage] = Field(default_factory=list)


class SearchQuery(BaseModel):
    query: str
    purpose: str


class ConversationContext(BaseModel):
    requirements: Requirements | None = None
    products: list[str] = Field(default_factory=list)
    last_response: str = ""
