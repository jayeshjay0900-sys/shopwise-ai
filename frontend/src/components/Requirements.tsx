import { Requirement } from '../types';

interface RequirementsProps {
  requirements: Requirement;
}

function Requirements({ requirements }: RequirementsProps) {
  const formatBudget = () => {
    if (requirements.budget_max) {
      if (requirements.budget_max >= 100000) {
        return `Under ₹${(requirements.budget_max / 100000).toFixed(1)} lakh`;
      }
      return `Under ₹${requirements.budget_max.toLocaleString('en-IN')}`;
    }
    if (requirements.budget_min) {
      return `Above ₹${requirements.budget_min.toLocaleString('en-IN')}`;
    }
    return 'No budget specified';
  };

  return (
    <div className="bg-white rounded-xl shadow-xl p-6">
      <h2 className="text-xl font-bold text-gray-800 mb-4">
        🎯 Detected Requirements
      </h2>
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
        {requirements.category && (
          <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-4 rounded-lg">
            <p className="text-xs text-gray-600 mb-1">Category</p>
            <p className="font-semibold text-blue-900 capitalize">{requirements.category}</p>
          </div>
        )}
        {requirements.brand && (
          <div className="bg-gradient-to-br from-purple-50 to-purple-100 p-4 rounded-lg">
            <p className="text-xs text-gray-600 mb-1">Brand</p>
            <p className="font-semibold text-purple-900">{requirements.brand}</p>
          </div>
        )}
        {requirements.model_family && (
          <div className="bg-gradient-to-br from-green-50 to-green-100 p-4 rounded-lg">
            <p className="text-xs text-gray-600 mb-1">Model</p>
            <p className="font-semibold text-green-900">{requirements.model_family}</p>
          </div>
        )}
        <div className="bg-gradient-to-br from-yellow-50 to-yellow-100 p-4 rounded-lg">
          <p className="text-xs text-gray-600 mb-1">Budget</p>
          <p className="font-semibold text-yellow-900">{formatBudget()}</p>
        </div>
        {requirements.use_case && (
          <div className="bg-gradient-to-br from-pink-50 to-pink-100 p-4 rounded-lg">
            <p className="text-xs text-gray-600 mb-1">Use Case</p>
            <p className="font-semibold text-pink-900 capitalize">{requirements.use_case}</p>
          </div>
        )}
      </div>
      {requirements.comparison_mode && (
        <div className="mt-4 p-3 bg-indigo-50 rounded-lg border-2 border-indigo-200">
          <p className="text-indigo-900 font-semibold">
            🔄 Comparison Mode: Comparing products
          </p>
        </div>
      )}
    </div>
  );
}

export default Requirements;
