import pytest
from backend.agents.shopping_agent import ShoppingAgent
from backend.models.search import ChatRequest
from backend.services.llm_service import LLMServiceError
from backend.services.tavily_service import TavilyServiceError


class FailingTavily:
    def build_queries(self, requirements): return [{"query": "x", "purpose": "x"}]
    async def search(self, query): raise TavilyServiceError("down")


@pytest.mark.asyncio
async def test_tavily_failure_is_translated():
    with pytest.raises(RuntimeError, match="Web research is temporarily unavailable"):
        await ShoppingAgent(tavily=FailingTavily()).run(ChatRequest(conversation_id="1", message="best phone"))


@pytest.mark.asyncio
async def test_empty_results_are_explicit():
    class EmptyTavily:
        def build_queries(self, requirements): return []
        async def search(self, query): return []
    result = await ShoppingAgent(tavily=EmptyTavily()).run(ChatRequest(conversation_id="1", message="best phone"))
    assert result.products == []
    assert "No reliable products" in result.assistant_message


def test_llm_error_type_exists():
    assert issubclass(LLMServiceError, RuntimeError)
