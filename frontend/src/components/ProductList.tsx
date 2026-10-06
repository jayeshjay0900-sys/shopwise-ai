import { Product } from '../types';

interface ProductListProps {
  products: Product[];
  comparisonMode: boolean;
}

function ProductList({ products, comparisonMode }: ProductListProps) {
  return (
    <div className="bg-white rounded-xl shadow-xl p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">
        {comparisonMode ? '⚖️ Product Comparison' : '🛍️ Top Products'}
      </h2>
      <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
        {products.map((product, index) => (
          <ProductCard key={index} product={product} rank={index + 1} />
        ))}
      </div>
    </div>
  );
}

interface ProductCardProps {
  product: Product;
  rank: number;
}

function ProductCard({ product, rank }: ProductCardProps) {
  const getRankBadge = () => {
    if (rank === 1) return '🥇 Best Match';
    if (rank === 2) return '🥈 Runner-up';
    if (rank === 3) return '🥉 Also Great';
    return `#${rank}`;
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'bg-green-500';
    if (score >= 60) return 'bg-yellow-500';
    return 'bg-orange-500';
  };

  return (
    <div className="border-2 border-gray-200 rounded-xl p-5 hover:shadow-lg transition-shadow bg-gradient-to-br from-white to-gray-50">
      {/* Rank Badge */}
      <div className="flex justify-between items-start mb-3">
        <span className="px-3 py-1 bg-gradient-to-r from-purple-500 to-blue-500 text-white text-sm font-bold rounded-full">
          {getRankBadge()}
        </span>
        <div className="flex items-center gap-2">
          <div className={`w-3 h-3 rounded-full ${getScoreColor(product.match_score)}`}></div>
          <span className="font-bold text-gray-700">{product.match_score.toFixed(0)}%</span>
        </div>
      </div>

      {/* Product Name */}
      <h3 className="text-lg font-bold text-gray-900 mb-2 line-clamp-2">
        {product.name}
      </h3>

      {/* Price */}
      {product.price ? (
        <p className="text-2xl font-bold text-green-600 mb-3">
          ₹{product.price.toLocaleString('en-IN')}
        </p>
      ) : (
        <p className="text-gray-500 mb-3">Price not available</p>
      )}

      {/* Source */}
      <a
        href={product.url}
        target="_blank"
        rel="noopener noreferrer"
        className="inline-block px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-semibold mb-4 transition-colors"
      >
        View on {product.source}
      </a>

      {/* Specifications */}
      {Object.keys(product.specifications).length > 0 && (
        <div className="mb-4">
          <p className="text-xs font-semibold text-gray-600 mb-2">SPECIFICATIONS</p>
          <div className="space-y-1">
            {Object.entries(product.specifications).slice(0, 3).map(([key, value]) => (
              <p key={key} className="text-sm text-gray-700">
                <span className="font-semibold capitalize">{key}:</span> {String(value)}
              </p>
            ))}
          </div>
        </div>
      )}

      {/* Pros */}
      {product.pros.length > 0 && (
        <div className="mb-3">
          <p className="text-xs font-semibold text-green-700 mb-2">✅ PROS</p>
          <ul className="space-y-1">
            {product.pros.slice(0, 3).map((pro, idx) => (
              <li key={idx} className="text-sm text-gray-700 flex items-start">
                <span className="text-green-600 mr-2">•</span>
                <span>{pro}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Cons */}
      {product.cons.length > 0 && (
        <div className="mb-3">
          <p className="text-xs font-semibold text-red-700 mb-2">❌ CONS</p>
          <ul className="space-y-1">
            {product.cons.slice(0, 2).map((con, idx) => (
              <li key={idx} className="text-sm text-gray-700 flex items-start">
                <span className="text-red-600 mr-2">•</span>
                <span>{con}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Review Sentiment */}
      {product.review_sentiment.available && (
        <div className="mt-4 pt-4 border-t border-gray-200">
          <p className="text-xs font-semibold text-gray-600 mb-2">📊 REVIEWS</p>
          <div className="flex gap-2 mb-2">
            {product.review_sentiment.positive_percentage !== null && (
              <div className="flex-1">
                <div className="bg-green-100 rounded-full h-2 overflow-hidden">
                  <div
                    className="bg-green-500 h-full"
                    style={{ width: `${product.review_sentiment.positive_percentage}%` }}
                  ></div>
                </div>
                <p className="text-xs text-gray-600 mt-1">
                  👍 {product.review_sentiment.positive_percentage.toFixed(0)}%
                </p>
              </div>
            )}
          </div>
          <p className="text-xs text-gray-600 italic">{product.review_sentiment.summary}</p>
        </div>
      )}
    </div>
  );
}

export default ProductList;
