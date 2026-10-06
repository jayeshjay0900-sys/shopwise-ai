import re
import json
from typing import List, Dict, Any, Optional
from groq import Groq
from models import ProductEvidence, Requirement, ReviewSentiment


class ProductProcessor:
    """
    Process search results into product evidence with strict validation.
    Uses LLM minimally for extraction, Python for validation.
    """

    def __init__(self, groq_client: Groq):
        self.groq_client = groq_client

    async def extract_products(
        self,
        search_results: List[Dict[str, Any]],
        requirement: Requirement
    ) -> List[ProductEvidence]:
        """
        Extract product evidence from search results.
        CRITICAL: Product, price, source, and URL must belong together.
        """
        products = []

        for result in search_results:
            try:
                # Extract using LLM with strict JSON output
                product_data = await self._extract_with_llm(result, requirement)

                if product_data:
                    # Validate price
                    if not self._is_valid_price(product_data.get('price')):
                        product_data['price'] = None

                    # Create product evidence
                    product = ProductEvidence(
                        name=product_data['name'],
                        price=product_data.get('price'),
                        url=result['url'],
                        source=self._extract_domain(result['url']),
                        specifications=product_data.get('specifications', {}),
                        description=product_data.get('description'),
                    )
                    products.append(product)
            except Exception as e:
                print(f"Error extracting product from {result.get('url', 'unknown')}: {e}")
                continue

        return products

    async def _extract_with_llm(
        self,
        search_result: Dict[str, Any],
        requirement: Requirement
    ) -> Optional[Dict[str, Any]]:
        """Use LLM to extract product information from search result"""

        prompt = f"""Extract product information from this search result. Return ONLY valid JSON.

Search Result:
Title: {search_result.get('title', '')}
Content: {search_result.get('content', '')}
URL: {search_result.get('url', '')}

Requirements:
- Category: {requirement.category or 'any'}
- Brand: {requirement.brand or 'any'}
- Model: {requirement.model_family or 'any'}

Extract:
1. Product name (exact, not generic like "Best Laptops")
2. Price in INR (numbers only, or null if not found)
3. Key specifications (processor, RAM, storage, etc.)
4. Brief description

Rules:
- Reject generic category pages (e.g., "Best Laptops Under 1 Lakh")
- Reject obviously wrong prices (₹0, ₹1, ₹2, ₹5, ₹10)
- Price must be for the SAME product as the name
- Return null if this is not a specific product page

Return JSON:
{{"name": "string", "price": number or null, "specifications": {{}}, "description": "string or null"}}"""

        try:
            response = self.groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
                max_tokens=500,
            )

            content = response.choices[0].message.content.strip()

            # Extract JSON from response
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())

                # Validate extracted data
                if data.get('name') and not self._is_generic_title(data['name']):
                    return data

            return None

        except Exception as e:
            print(f"LLM extraction error: {e}")
            return None

    def _is_generic_title(self, title: str) -> bool:
        """Check if title is a generic category page"""
        generic_patterns = [
            r'^best\s+\w+',
            r'^top\s+\d+',
            r'^\d+\s+best',
            r'laptop\s+under',
            r'phone\s+under',
            r'best\s+deals',
            r'buying\s+guide',
        ]

        title_lower = title.lower()
        return any(re.search(pattern, title_lower) for pattern in generic_patterns)

    def _is_valid_price(self, price: Optional[float]) -> bool:
        """
        Validate price to reject corrupted values.
        CRITICAL: Reject ₹0, ₹1, ₹2, ₹5, ₹10 unless strong evidence.
        """
        if price is None:
            return False

        # Reject obviously corrupted prices
        if price <= 10:
            return False

        # Reject unreasonably high prices (> 10 crore)
        if price > 100000000:
            return False

        return True

    def _extract_domain(self, url: str) -> str:
        """Extract clean domain name from URL"""
        match = re.search(r'(?:https?://)?(?:www\.)?([^/]+)', url)
        if match:
            domain = match.group(1)
            # Clean up common patterns
            domain = domain.replace('www.', '')
            return domain
        return url

    async def analyze_reviews(
        self,
        product_name: str,
        search_results: List[Dict[str, Any]]
    ) -> ReviewSentiment:
        """
        Analyze reviews for a product.
        CRITICAL: Never fabricate reviews. Return unavailable if insufficient data.
        """

        # Find review content
        review_content = []
        for result in search_results:
            content = result.get('content', '')
            title = result.get('title', '')

            # Check if this looks like a review
            if any(word in title.lower() for word in ['review', 'rating', 'opinion']):
                review_content.append(content)

        if not review_content:
            return ReviewSentiment(available=False)

        try:
            # Use LLM to analyze sentiment
            prompt = f"""Analyze review sentiment for {product_name}.

Review Content:
{' '.join(review_content[:3])}

Provide:
1. Positive percentage (0-100)
2. Negative percentage (0-100)
3. Neutral percentage (0-100)
4. Brief summary

Rules:
- Percentages must sum to 100
- Base ONLY on provided content
- If insufficient data, return all null

Return JSON:
{{"positive": number or null, "negative": number or null, "neutral": number or null, "summary": "string"}}"""

            response = self.groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
                max_tokens=300,
            )

            content = response.choices[0].message.content.strip()
            json_match = re.search(r'\{.*\}', content, re.DOTALL)

            if json_match:
                data = json.loads(json_match.group())

                # Validate data
                pos = data.get('positive')
                neg = data.get('negative')
                neu = data.get('neutral')

                if pos is not None and neg is not None and neu is not None:
                    # Check if percentages are reasonable
                    total = pos + neg + neu
                    if 95 <= total <= 105:  # Allow small rounding errors
                        return ReviewSentiment(
                            positive_percentage=pos,
                            negative_percentage=neg,
                            neutral_percentage=neu,
                            summary=data.get('summary', 'Review analysis available'),
                            available=True,
                        )

            return ReviewSentiment(available=False)

        except Exception as e:
            print(f"Review analysis error: {e}")
            return ReviewSentiment(available=False)
