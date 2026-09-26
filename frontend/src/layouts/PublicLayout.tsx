import { Outlet } from "react-router-dom";

export function PublicLayout() {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-2xl font-bold text-gray-900">Edu-Branch-AI"text-sm text-gray-500 mt-1">AI Platform for Interactive Case Studies</p>
        </div>
        <Outlet />
      </div>
    </div>
  );
}
