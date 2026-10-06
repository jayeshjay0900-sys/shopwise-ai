function LoadingState() {
  return (
    <div className="bg-white rounded-xl shadow-xl p-12 text-center">
      <div className="flex flex-col items-center gap-4">
        <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-purple-600"></div>
        <div className="space-y-2">
          <p className="text-xl font-semibold text-gray-800">
            🔍 Searching for the best products...
          </p>
          <p className="text-gray-600">
            Analyzing requirements and gathering results
          </p>
        </div>
      </div>
    </div>
  );
}

export default LoadingState;
