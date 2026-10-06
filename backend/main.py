import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from groq import Groq
import traceback

from models import SearchQuery, SearchResponse, Requirement
from requirement_extractor import RequirementExtractor
from tavily_researcher import TavilyResearcher
from product_processor import ProductProcessor
from product_filter import ProductFilter
from product_scorer import ProductScorer
from recommendation_generator import RecommendationGenerator

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI(title="ShopWise AI", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for frontend (if they exist)
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/assets", StaticFiles(directory=os.path.join(static_dir, "assets")), name="assets")

# Initialize services
try:
    groq_api_key = os.getenv("GROQ_API_KEY")
    tavily_api_key = os.getenv("TAVILY_API_KEY")

    if not groq_api_key or not tavily_api_key:
        raise ValueError("Missing API keys in .env file")

    groq_client = Groq(api_key=groq_api_key)

    # Initialize components
    requirement_extractor = RequirementExtractor()
    tavily_researcher = TavilyResearcher(tavily_api_key)
    product_processor = ProductProcessor(groq_client)
    product_filter = ProductFilter()
    product_scorer = ProductScorer()
    recommendation_generator = RecommendationGenerator(groq_client)

except Exception as e:
    print(f"Initialization error: {e}")
    groq_client = None


@app.get("/")
async def root():
    """Serve frontend or health check"""
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    index_file = os.path.join(static_dir, "index.html")

    # Serve frontend if it exists, otherwise API info
    if os.path.exists(index_file):
        return FileResponse(index_file)

    return {
        "status": "running",
        "service": "ShopWise AI",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "groq_configured": groq_client is not None,
        "tavily_configured": tavily_api_key is not None,
    }


@app.post("/search", response_model=SearchResponse)
async def search(query: SearchQuery):
    """
    Main search endpoint.

    Flow:
    1. Extract requirements
    2. Validate
    3. Research with Tavily
    4. Extract products
    5. Hard filter
    6. Analyze reviews
    7. Score and rank
    8. Generate recommendation
    """

    if not groq_client:
        raise HTTPException(status_code=500, detail="API keys not configured")

    try:
        # Step 1: Extract requirements
        requirements = requirement_extractor.extract(query.query)

        # Step 2: Validate requirements
        if not requirements.category and not requirements.brand and not requirements.comparison_mode:
            return SearchResponse(
                query=query.query,
                requirements=requirements,
                products=[],
                recommendation="Please provide more details about what product you're looking for (e.g., laptop, phone, or specific brand).",
                comparison_mode=False,
                error="Insufficient search criteria"
            )

        # Step 3: Research with Tavily (minimized calls)
        search_results = await tavily_researcher.research(requirements, query.query)

        if not search_results:
            return SearchResponse(
                query=query.query,
                requirements=requirements,
                products=[],
                recommendation="No results found. Try broadening your search or checking your spelling.",
                comparison_mode=requirements.comparison_mode,
                error="No search results"
            )

        # Step 4: Extract products from results
        product_evidence = await product_processor.extract_products(search_results, requirements)

        if not product_evidence:
            return SearchResponse(
                query=query.query,
                requirements=requirements,
                products=[],
                recommendation="Could not extract product information from search results. Try a different query.",
                comparison_mode=requirements.comparison_mode,
                error="Product extraction failed"
            )

        # Step 5: Apply HARD filters BEFORE ranking
        filtered_products = product_filter.filter(product_evidence, requirements)

        if not filtered_products:
            # Generate helpful message about why filtering failed
            rec_msg = recommendation_generator._generate_no_results_message(requirements)
            return SearchResponse(
                query=query.query,
                requirements=requirements,
                products=[],
                recommendation=rec_msg,
                comparison_mode=requirements.comparison_mode,
                error="No products match filters"
            )

        # Step 6: Analyze reviews (optional, only for top products)
        review_sentiments = {}
        for product in filtered_products[:3]:  # Only analyze top 3
            sentiment = await product_processor.analyze_reviews(product.name, search_results)
            review_sentiments[product.name] = sentiment

        # Step 7: Score and rank deterministically
        ranked_products = product_scorer.score_and_rank(
            filtered_products,
            requirements,
            review_sentiments
        )

        # Limit to top 5 results
        ranked_products = ranked_products[:5]

        # Step 8: Generate recommendation
        recommendation = await recommendation_generator.generate(
            query.query,
            requirements,
            ranked_products,
            requirements.comparison_mode
        )

        return SearchResponse(
            query=query.query,
            requirements=requirements,
            products=ranked_products,
            recommendation=recommendation,
            comparison_mode=requirements.comparison_mode,
            error=None
        )

    except Exception as e:
        print(f"Search error: {e}")
        print(traceback.format_exc())

        # Return graceful error response
        return SearchResponse(
            query=query.query,
            requirements=Requirement(),
            products=[],
            recommendation=f"An error occurred while processing your search. Please try again.",
            comparison_mode=False,
            error=str(e)
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
