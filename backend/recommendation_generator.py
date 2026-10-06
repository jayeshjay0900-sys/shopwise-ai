from typing import List
from groq import Groq
from models import Product, Requirement
import json


class RecommendationGenerator:
    """Generate natural language recommendations using LLM"""

    def __init__(self, groq_client: Groq):
        self.groq_client = groq_client

    async def generate(
        self,
        query: str,
        requirement: Requirement,
        products: List[Product],
        comparison_mode: bool = False
    ) -> str:
        """Generate final recommendation"""

        if not products:
            return self._generate_no_results_message(requirement)

        if comparison_mode:
            return await self._generate_comparison(query, products)

        return await self._generate_recommendation(query, requirement, products)

    def _generate_no_results_message(self, requirement: Requirement) -> str:
        """Generate helpful message when no products found"""
        msg = "I couldn't find products matching your requirements. "

        suggestions = []
        if requirement.budget_max:
            suggestions.append("try increasing your budget")
        if requirement.brand:
            suggestions.append("try different brands")
        if requirement.model_family:
            suggestions.append("broaden your model search")

        if suggestions:
            msg += "Consider: " + ", ".join(suggestions) + "."

        return msg

    async def _generate_recommendation(
        self,
        query: str,
        requirement: Requirement,
        products: List[Product]
    ) -> str:
        """Generate recommendation for regular search"""

        # Prepare product summaries
        product_summaries = []
        for i, product in enumerate(products[:3], 1):
            summary = f"{i}. {product.name}"
            if product.price:
                summary += f" - ₹{int(product.price):,}"
            summary += f" (Match: {product.match_score:.0f}%)"
            product_summaries.append(summary)

        prompt = f"""Generate a concise shopping recommendation.

Query: {query}

Requirements:
- Budget: {self._format_budget(requirement)}
- Brand: {requirement.brand or 'Any'}
- Category: {requirement.category or 'Any'}
- Use case: {requirement.use_case or 'General'}

Top Products:
{chr(10).join(product_summaries)}

Provide:
1. Best overall pick (1-2 sentences)
2. Why it's the best choice
3. Brief mention of alternatives

Keep it concise and actionable. 3-4 sentences total."""

        try:
            response = self.groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=200,
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"Recommendation generation error: {e}")
            # Fallback
            best = products[0]
            msg = f"Based on your requirements, I recommend the {best.name}"
            if best.price:
                msg += f" at ₹{int(best.price):,}"
            msg += f". It has the highest match score ({best.match_score:.0f}%) for your needs."
            return msg

    async def _generate_comparison(self, query: str, products: List[Product]) -> str:
        """Generate comparison between products"""

        if len(products) < 2:
            return "I need at least 2 products to compare. Please refine your search."

        # Prepare product data
        product_data = []
        for product in products[:2]:
            data = {
                "name": product.name,
                "price": f"₹{int(product.price):,}" if product.price else "N/A",
                "specs": product.specifications,
                "pros": product.pros[:3],
                "cons": product.cons[:2],
            }
            product_data.append(data)

        prompt = f"""Compare these two products concisely.

Product 1: {product_data[0]['name']}
Price: {product_data[0]['price']}
Key pros: {', '.join(product_data[0]['pros'][:2])}

Product 2: {product_data[1]['name']}
Price: {product_data[1]['price']}
Key pros: {', '.join(product_data[1]['pros'][:2])}

Provide:
1. Key differences (1-2 points)
2. Which is better for what use case
3. Clear recommendation

Keep it concise. 3-4 sentences total."""

        try:
            response = self.groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=200,
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"Comparison generation error: {e}")
            # Fallback
            return f"Comparing {products[0].name} vs {products[1].name}. Check the detailed specifications and match scores above for a thorough comparison."

    def _format_budget(self, requirement: Requirement) -> str:
        """Format budget for display"""
        if requirement.budget_max:
            if requirement.budget_max >= 100000:
                return f"Under ₹{requirement.budget_max/100000:.1f} lakh"
            else:
                return f"Under ₹{int(requirement.budget_max):,}"
        elif requirement.budget_min:
            return f"Above ₹{int(requirement.budget_min):,}"
        else:
            return "No budget specified"
