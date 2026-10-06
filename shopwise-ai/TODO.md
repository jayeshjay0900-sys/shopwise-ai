# SHOPWISE AI — Delivery Outcomes

## Dynamic research-backed shopping agent
Build a real AI shopping chatbot—not a static UI demo and not a hardcoded product list—that accepts natural-language shopping requests, extracts product category, budget, currency, use case, requirements, preferences, exclusions, and comparison targets; dynamically generates research queries; searches real web information; discovers and deduplicates products; extracts verified information; analyzes reviews; scores and ranks options; generates recommendations; and returns a structured response to the chat UI.

## Evidence, data integrity, and links
Use Pydantic models for products containing name, brand, price, currency, rating, review count, image URL, specifications, pros, cons, review summary, sentiment, match score, product URL, review URLs, and source URLs. Never fabricate missing information; show `Not available` when unverifiable. Every displayed product must have a verified real product URL that opens in a new tab; every displayed review link must be a verified real review source; never invent URLs. Show verified information separately from ShopWise AI analysis, preserve evidence source links, show multiple retailer/official prices with direct links where available, and include `Prices can change. Check the retailer before purchasing.`

## Explainable recommendations and comparison
Provide an explainable ShopWise Match Score based on budget, required features, preferences, use case, product quality, and review signals. Explain the score and include `AI-generated score based on your requirements and available product evidence.` Highlight a ShopWise Recommendation with product, price, match, rationale, View Product, Read Reviews, and Compare actions. Support comparison tables and Best Overall, Best Value, Best Performance, and Best for Your Use Case conclusions.

## Conversation memory
Preserve current conversation context so follow-up questions such as `Which is best for deep learning?`, `What about battery?`, and `Show alternatives.` work without repeating requirements. Alternatives should research with existing constraints.

## Professional responsive frontend
Deliver a minimal, modern, clean, professional, neutral, responsive, mobile-friendly React/TypeScript/Tailwind interface with ShopWise AI branding, the tagline `Shop smarter. Let AI research for you.`, natural-language composer, category prompts for Phones, Laptops, Headphones, and Cameras, conversation thread, staged research loading, responsive product cards, featured recommendation, evidence panels, sentiment bars, comparison, keyboard focus states, restrained animation, and exact empty/provider-failure states. Do not use excessive gradients, huge dashboards, fake futuristic effects, or student-project styling.

## Modular FastAPI backend and provider handling
Implement the specified modular backend structure with FastAPI, Pydantic, Groq structured JSON outputs, Tavily web research, product/review services, scoring, validation, and an orchestrating shopping agent. Keep API keys server-side using `TAVILY_API_KEY` and `GROQ_API_KEY`; include `.env.example`, ignore `.env`, and never commit secrets. Translate failures exactly: `Web research is temporarily unavailable.`, `The AI analysis service is temporarily unavailable.`, and `No reliable products were found matching your requirements.` Never generate fake fallback products.

## Tests and engineering quality
Add pytest coverage for requirement extraction, product validation, match scoring, empty search results, invalid product data, missing URLs, API failure, LLM failure, and Tavily failure. Use type hints, response validation, bounded provider timeouts, error handling, useful comments, clean dependencies, no debug prints, no unused files, and no browser-exposed keys. Ensure the frontend builds, backend starts, and tests pass.

## Documentation and GitHub readiness
Create `README.md` with Demo placeholder, features, architecture flow, tech stack, stage-by-stage operation, exact local installation commands, environment variables, example queries, engineering highlights, limitations, future improvements, security notes, project description, and GitHub topics. Create `docs/architecture.md` covering request/response flow, evidence boundaries, scoring, provider failures, and SQLite/PostgreSQL readiness. Include `public/manus-routes.json`, root `Dockerfile`, `requirements.txt`, `package.json`, and a clean GitHub-ready structure.

## Deployment and release
Use a reproducible multi-stage Docker build with a Node frontend build stage and slim Python/FastAPI runtime stage. Bind to `0.0.0.0`, honor `PORT` with a 3000 default, serve the compiled frontend and SPA fallback from FastAPI, expose unauthenticated `GET /api/health`, keep provider keys runtime-only, configure the Webdev deployment declaration with server capability, preserve reserved routes, verify health, route manifest, SPA root, API semantics, tests, and build, then commit and push intended files to canonical `origin/main` without force-pushing. Publish only after a verified checkpoint and successful public health check; otherwise deliver the stable Preview as a preview.
