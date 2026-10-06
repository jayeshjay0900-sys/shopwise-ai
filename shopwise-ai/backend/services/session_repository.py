from __future__ import annotations

from dataclasses import dataclass, field
from backend.models.product import Product
from backend.models.search import Requirements


@dataclass
class ConversationState:
    requirements: Requirements | None = None
    products: list[Product] = field(default_factory=list)


class InMemoryConversationRepository:
    def __init__(self) -> None:
        self._states: dict[str, ConversationState] = {}

    def get(self, conversation_id: str) -> ConversationState:
        return self._states.get(conversation_id, ConversationState())

    def save(self, conversation_id: str, requirements: Requirements, products: list[Product]) -> None:
        self._states[conversation_id] = ConversationState(requirements=requirements, products=products)
