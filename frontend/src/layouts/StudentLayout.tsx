import { Outlet } from "react-router-dom";

/** Student simulator layout. */
export function StudentLayout() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* TODO: Add student navigation in feature/ui-student-layout */}
      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <h1 className="text-lg font-semibold text-gray-900">CaseTree AI — Simulator</h1>
      </header>
      <main className="max-w-4xl mx-auto px-6 py-8">
        <Outlet />
      </main>
    </div>
  );
}
