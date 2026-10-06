import { useState } from 'react';
import { api } from './api';
import { SearchResponse } from './types';
import SearchBar from './components/SearchBar';
import Requirements from './components/Requirements';
import ProductList from './components/ProductList';
import Recommendation from './components/Recommendation';
import LoadingState from './components/LoadingState';
import ErrorMessage from './components/ErrorMessage';

function App() {
  const [searchResponse, setSearchResponse] = useState<SearchResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (query: string) => {
    if (!query.trim()) return;

    setLoading(true);
    setError(null);
    setSearchResponse(null);

    try {
      const response = await api.search(query);
      setSearchResponse(response);

      if (response.error) {
        setError(response.error);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'An error occurred while searching');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen py-8 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-white mb-4">
            🛍️ ShopWise AI
          </h1>
          <p className="text-xl text-white/90">
            Your Intelligent Shopping Assistant
          </p>
          <p className="text-white/70 mt-2">
            Powered by AI • Accurate Results • Smart Recommendations
          </p>
        </div>

        {/* Search Bar */}
        <SearchBar onSearch={handleSearch} loading={loading} />

        {/* Loading State */}
        {loading && <LoadingState />}

        {/* Error Message */}
        {error && !searchResponse && <ErrorMessage message={error} />}

        {/* Results */}
        {searchResponse && !loading && (
          <div className="space-y-6">
            {/* Requirements */}
            <Requirements requirements={searchResponse.requirements} />

            {/* Products */}
            {searchResponse.products.length > 0 ? (
              <>
                <ProductList
                  products={searchResponse.products}
                  comparisonMode={searchResponse.comparison_mode}
                />

                {/* Recommendation */}
                <Recommendation
                  recommendation={searchResponse.recommendation}
                  comparisonMode={searchResponse.comparison_mode}
                />
              </>
            ) : (
              <div className="bg-white rounded-xl shadow-xl p-8 text-center">
                <p className="text-gray-600 text-lg">
                  {searchResponse.recommendation || 'No products found matching your criteria.'}
                </p>
              </div>
            )}
          </div>
        )}

        {/* Footer */}
        <div className="text-center mt-12 text-white/70 text-sm">
          <p>Built with React, TypeScript, FastAPI, Groq AI & Tavily</p>
        </div>
      </div>
    </div>
  );
}

export default App;
