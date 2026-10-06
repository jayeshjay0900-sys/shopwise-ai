interface ErrorMessageProps {
  message: string;
}

function ErrorMessage({ message }: ErrorMessageProps) {
  return (
    <div className="bg-red-50 border-2 border-red-200 rounded-xl shadow-xl p-8 text-center">
      <div className="flex flex-col items-center gap-4">
        <div className="text-6xl">⚠️</div>
        <div className="space-y-2">
          <p className="text-xl font-semibold text-red-800">
            Error
          </p>
          <p className="text-red-600">
            {message}
          </p>
        </div>
      </div>
    </div>
  );
}

export default ErrorMessage;
