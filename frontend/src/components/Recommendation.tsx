interface RecommendationProps {
  recommendation: string;
  comparisonMode: boolean;
}

function Recommendation({ recommendation, comparisonMode }: RecommendationProps) {
  return (
    <div className="bg-gradient-to-r from-purple-600 to-blue-600 rounded-xl shadow-xl p-8 text-white">
      <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
        {comparisonMode ? '🔄 Comparison Summary' : '💡 AI Recommendation'}
      </h2>
      <p className="text-lg leading-relaxed">{recommendation}</p>
    </div>
  );
}

export default Recommendation;
