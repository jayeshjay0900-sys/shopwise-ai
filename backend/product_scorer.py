from typing import List
from models import ProductEvidence, Requirement, Product, ReviewSentiment


class ProductScorer:
    """
    Deterministic scoring system using Python logic.
    LLM used only for natural language understanding, not scoring.
    """

    def score_and_rank(
        self,
        products: List[ProductEvidence],
        requirement: Requirement,
        review_sentiments: dict = None
    ) -> List[Product]:
        """Score products and rank them deterministically"""

        if review_sentiments is None:
            review_sentiments = {}

        scored_products = []

        for product in products:
            # Calculate match score
            score = self._calculate_score(product, requirement)

            # Get review sentiment
            sentiment = review_sentiments.get(product.name, ReviewSentiment(available=False))

            # Generate pros and cons
            pros, cons = self._generate_pros_cons(product, requirement)

            # Create final product
            final_product = Product(
                name=product.name,
                price=product.price,
                currency=product.currency,
                url=product.url,
                source=product.source,
                specifications=product.specifications,
                pros=pros,
                cons=cons,
                match_score=score,
                review_sentiment=sentiment,
                evidence_urls=[product.url],
            )

            scored_products.append(final_product)

        # Sort by score (descending)
        scored_products.sort(key=lambda p: p.match_score, reverse=True)

        return scored_products

    def _calculate_score(self, product: ProductEvidence, requirement: Requirement) -> float:
        """
        Deterministic scoring algorithm.
        Score range: 0-100
        """
        score = 50.0  # Base score

        # Brand match (20 points)
        if requirement.brand:
            if requirement.brand.lower() in product.name.lower():
                score += 20

        # Model match (20 points)
        if requirement.model_family:
            if requirement.model_family.lower() in product.name.lower():
                score += 20

        # Budget optimization (15 points)
        if requirement.budget_max and product.price:
            # Reward products that use budget efficiently
            utilization = product.price / requirement.budget_max
            if 0.7 <= utilization <= 1.0:
                score += 15  # Sweet spot: 70-100% of budget
            elif 0.5 <= utilization < 0.7:
                score += 10  # Good value
            elif utilization < 0.5:
                score += 5   # Very cheap (might lack features)

        # Has price data (10 points) - products with prices are more reliable
        if product.price:
            score += 10

        # Has specifications (10 points)
        if product.specifications:
            score += min(len(product.specifications) * 2, 10)

        # Source reliability (5 points)
        trusted_sources = ['amazon.in', 'flipkart.com', 'croma.com']
        if any(source in product.source.lower() for source in trusted_sources):
            score += 5

        # Cap at 100
        return min(score, 100.0)

    def _generate_pros_cons(
        self,
        product: ProductEvidence,
        requirement: Requirement
    ) -> tuple[List[str], List[str]]:
        """Generate pros and cons based on specifications and requirements"""

        pros = []
        cons = []

        # Price-based pros/cons
        if product.price and requirement.budget_max:
            utilization = product.price / requirement.budget_max
            if utilization < 0.7:
                pros.append(f"Great value at ₹{int(product.price):,}")
            elif utilization > 0.95:
                cons.append("Near upper budget limit")

        # Brand match
        if requirement.brand and requirement.brand.lower() in product.name.lower():
            pros.append(f"Matches requested brand ({requirement.brand})")

        # Model match
        if requirement.model_family and requirement.model_family.lower() in product.name.lower():
            pros.append(f"Exact model match ({requirement.model_family})")

        # Specifications-based pros
        specs = product.specifications
        if specs:
            # Check for key specifications
            if 'processor' in specs:
                pros.append(f"Processor: {specs['processor']}")

            if 'ram' in specs:
                pros.append(f"RAM: {specs['ram']}")

            if 'storage' in specs:
                pros.append(f"Storage: {specs['storage']}")

        # Source reliability
        if 'amazon.in' in product.source or 'flipkart.com' in product.source:
            pros.append("Available on trusted platform")

        # Generic cons if no price
        if not product.price:
            cons.append("Price information not available")

        # Ensure at least some content
        if not pros:
            pros.append("Meets search criteria")

        if not cons and product.price:
            cons.append("Limited information available")

        return pros[:5], cons[:3]  # Limit length
