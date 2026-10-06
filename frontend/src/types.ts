export interface Requirement {
  category: string | null;
  brand: string | null;
  model_family: string | null;
  budget_min: number | null;
  budget_max: number | null;
  must_have_features: string[];
  use_case: string | null;
  comparison_mode: boolean;
  comparison_products: string[];
}

export interface ReviewSentiment {
  positive_percentage: number | null;
  negative_percentage: number | null;
  neutral_percentage: number | null;
  summary: string;
  available: boolean;
}

export interface Product {
  name: string;
  price: number | null;
  currency: string;
  url: string;
  source: string;
  image_url: string | null;
  specifications: Record<string, any>;
  pros: string[];
  cons: string[];
  match_score: number;
  review_sentiment: ReviewSentiment;
  evidence_urls: string[];
}

export interface SearchResponse {
  query: string;
  requirements: Requirement;
  products: Product[];
  recommendation: string;
  comparison_mode: boolean;
  error: string | null;
}

export interface SearchRequest {
  query: string;
}
