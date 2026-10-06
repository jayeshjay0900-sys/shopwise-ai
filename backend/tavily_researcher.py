import os
import httpx
from typing import List, Dict, Any, Optional
from models import Requirement


class TavilyResearcher:
    """Handles Tavily API research with focused queries"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.tavily.com/search"

    async def research(self, requirement: Requirement, query: str) -> List[Dict[str, Any]]:
        """
        Execute focused Tavily search based on requirements.
        Minimizes API calls by constructing precise queries.
        """
        search_queries = self._build_search_queries(requirement, query)

        all_results = []
        async with httpx.AsyncClient(timeout=30.0) as client:
            for search_query in search_queries:
                try:
                    results = await self._execute_search(client, search_query)
                    all_results.extend(results)
                except Exception as e:
                    print(f"Search error for '{search_query}': {e}")
                    continue

        return all_results

    def _build_search_queries(self, requirement: Requirement, original_query: str) -> List[str]:
        """
        Build focused search queries to minimize API calls.
        Maximum 2-3 queries per search.
        """
        queries = []

        # Comparison mode - search for each product
        if requirement.comparison_mode and requirement.comparison_products:
            for product in requirement.comparison_products[:2]:  # Limit to 2 products
                query = f"{product} India price specifications reviews"
                queries.append(query)
            return queries

        # Build focused query
        parts = []

        if requirement.brand:
            parts.append(requirement.brand)

        if requirement.model_family:
            parts.append(requirement.model_family)
        elif requirement.category:
            parts.append(requirement.category)

        if requirement.use_case:
            parts.append(f"for {requirement.use_case}")

        # Add budget to query context
        if requirement.budget_max:
            if requirement.budget_max >= 100000:
                parts.append(f"under {requirement.budget_max/100000:.1f} lakh")
            else:
                parts.append(f"under ₹{int(requirement.budget_max)}")

        # Primary query
        main_query = " ".join(parts) + " India price specifications"
        queries.append(main_query)

        # Add review query if needed (only for specific products)
        if requirement.brand and requirement.model_family:
            review_query = f"{requirement.brand} {requirement.model_family} reviews India"
            queries.append(review_query)

        return queries[:2]  # Maximum 2 queries

    async def _execute_search(self, client: httpx.AsyncClient, query: str) -> List[Dict[str, Any]]:
        """Execute single Tavily search"""
        payload = {
            "api_key": self.api_key,
            "query": query,
            "search_depth": "basic",
            "max_results": 5,
            "include_domains": [
                "amazon.in",
                "flipkart.com",
                "croma.com",
                "reliance.com",
                "vijaysales.com",
                "smartprix.com",
                "91mobiles.com",
                "gadgets360.com",
                "digit.in",
            ],
        }

        response = await client.post(self.base_url, json=payload)
        response.raise_for_status()

        data = response.json()
        return data.get("results", [])
