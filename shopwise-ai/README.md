# ShopWise AI

> ShopWise AI is an AI-powered shopping research agent that combines web search, LLM-based information extraction, review intelligence, and personalized recommendation scoring to help users make better purchasing decisions.

## Demo

**Deployed application:** _Add the published URL here after deployment._

## Features

- AI shopping chatbot for natural-language buying decisions
- Dynamic Tavily web research and source evidence
- Product discovery, deduplication, and validation
- Groq structured information extraction
- Review intelligence and sentiment analysis
- Explainable ShopWise Match Score
- Personalized recommendations and comparison tables
- Verified product links and review links
- Conversation memory for follow-up questions
- Clear separation between verified information and AI analysis
- Responsive, professional React interface

## Architecture

```text
User
 ↓
React + TypeScript Chat UI
 ↓
FastAPI
 ↓
Shopping Agent
 ↓
Tavily Web Research
 ↓
Product Evidence
 ↓
Groq Structured LLM
 ↓
Review Analysis + Sentiment
 ↓
Recommendation Engine + Match Score
 ↓
Structured Response
 ↓
Evidence-forward React UI
```

## Tech stack

React · TypeScript · Tailwind CSS · Vite · FastAPI · Python · Pydantic · Groq · Tavily · SQLite-ready repository boundary · pytest · Docker

## How it works

1. **Requirement extraction** turns a natural-language request into category, budget, use case, constraints, and preferences.
2. **Search generation** creates focused product, specification, review, and price queries.
3. **Web retrieval** collects multiple sources, prioritizing manufacturers, retailers, and reputable technology publications.
4. **Product normalization** deduplicates results and rejects records without a verified URL.
5. **Structured extraction** asks Groq to normalize only facts present in bounded, labelled evidence.
6. **Review intelligence** summarizes what buyers like, common complaints, and sentiment percentages.
7. **Scoring and ranking** calculates an explainable match score from the user’s requirements and available signals.
8. **Recommendation** highlights the strongest overall choice and provides comparison rows and source links.
9. **Conversation memory** keeps active requirements available to follow-up questions and alternatives.

## Installation

```bash
git clone <your-repository-url>
cd shopwise-ai
npm install
python3 -m pip install -r requirements.txt
cp .env.example .env
```

Add `TAVILY_API_KEY` and `GROQ_API_KEY` to `.env` for live research.

### Run frontend development mode

```bash
npm run dev
```

### Run the production-style FastAPI app

```bash
npm run build
uvicorn backend.main:app --host 0.0.0.0 --port 3000
```

Open `http://localhost:3000`.

### Deployment

The root `Dockerfile` builds the Vite frontend and runs FastAPI on `0.0.0.0:${PORT:-3000}`. The managed deployment declaration uses `Dockerfile` with `/api/health` as its unauthenticated health path. Configure `TAVILY_API_KEY` and `GROQ_API_KEY` as runtime secrets in the hosting environment; they are intentionally not required during image compilation.

## Environment variables

- `TAVILY_API_KEY`: server-side Tavily web research key.
- `GROQ_API_KEY`: server-side Groq structured-output key.
- `GROQ_MODEL`: optional Groq model override.
- `PORT`: runtime port, defaults to `3000`.

Never put provider keys in frontend code. `.env` is ignored; `.env.example` is safe to commit.

## Example queries

- “Best phone under ₹50,000”
- “Gaming laptop under ₹1 lakh”
- “Best headphones under ₹10,000”
- “I need a laptop for machine learning with NVIDIA graphics and at least 16GB RAM.”
- “Compare these two phones.”

## Engineering highlights

- Modular agent architecture with separable parser, research, review, ranking, and provider services.
- Structured LLM outputs guarded by Pydantic response validation.
- Evidence-first retrieval with verified URLs and source provenance.
- Deterministic, explainable recommendation scoring rather than opaque ranking alone.
- Server-side API key handling and explicit provider failure semantics.
- Typed React contracts that mirror FastAPI responses.
- Test coverage for parser, validation, scoring, empty results, and provider failures.
- Docker-ready production runtime with FastAPI serving the compiled frontend.
- Repository boundary that keeps active conversation state replaceable with SQLite/PostgreSQL.

## Limitations

Prices can change after research. Web information may become outdated or unavailable. AI recommendations are not guarantees. Source availability varies by retailer, region, and page accessibility. Results without reliable evidence are omitted rather than fabricated.

## Future improvements

- User authentication and saved products
- Price history and price alerts
- Affiliate links with transparent disclosure
- Multi-agent research specialization
- Better review extraction and aspect sentiment
- Durable product/evidence database
- Offline evaluation framework and ranking benchmarks
- Deeper recommendation personalization

## GitHub topics

`ai` `generative-ai` `llm` `ai-agent` `shopping-agent` `recommendation-system` `rag` `web-search` `fastapi` `react` `python` `groq` `tavily` `sentiment-analysis` `machine-learning`
