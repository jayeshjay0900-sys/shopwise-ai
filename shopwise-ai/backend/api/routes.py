from __future__ import annotations
import logging
from fastapi import APIRouter, HTTPException
from backend.agents.shopping_agent import ShoppingAgent
from backend.models.recommendation import ChatResponse
from backend.models.search import ChatRequest
from backend.services.session_repository import InMemoryConversationRepository

router = APIRouter(prefix="/api")
agent = ShoppingAgent()
sessions = InMemoryConversationRepository()
logger = logging.getLogger("shopwise.api")

@router.get("/health")
async def health() -> dict[str, str]: return {"status": "ok", "service": "shopwise-ai"}

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    state = sessions.get(request.conversation_id)
    try:
        response = await agent.run(request, state.requirements, state.products)
        sessions.save(request.conversation_id, response.requirements, response.products)
        return response
    except RuntimeError as exc:
        logger.warning("Known chat failure: %s", str(exc))
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Unexpected chat failure: %s", type(exc).__name__)
        raise HTTPException(status_code=503, detail="The AI analysis service is temporarily unavailable.") from exc
