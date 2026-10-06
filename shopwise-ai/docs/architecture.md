# ShopWise AI Architecture

## Request flow

```text
React Chat UI → FastAPI /api/chat → ShoppingAgent
  → RequirementParser
  → TavilyService (dynamic searches)
  → ProductService (deduplication + evidence normalization)
  → Groq structured extraction
  → ReviewAnalyzer (sentiment + summaries)
  → deterministic scoring + Recommender
  → typed ChatResponse → React evidence UI
```

## Evidence boundary

Search results are the only allowed source for product facts. Every product retains source URLs and evidence snippets. The LLM may normalize and summarize bounded, source-labelled evidence, but it may not invent missing facts or links. The UI labels verified information separately from ShopWise AI analysis.

## Scoring

The score combines budget fit, required/preferred feature coverage, product quality, and review signals. It is an explainable prioritization aid, not an objective truth. Each result carries a short explanation and the response includes the disclaimer: `AI-generated score based on your requirements and available product evidence.`

## Provider failures

- Tavily failure → `Web research is temporarily unavailable.`
- Groq failure → `The AI analysis service is temporarily unavailable.`
- Verified empty result → `No reliable products were found matching your requirements.`

The frontend treats these as first-class states and never falls back to fabricated catalog items.

## Persistence boundary

The first release stores active conversation requirements in a process-local session map keyed by a browser-generated conversation ID. The route contract is intentionally independent of storage so the map can be replaced with SQLite/PostgreSQL tables for conversations, evidence, products, and recommendation runs.
