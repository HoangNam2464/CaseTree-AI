import { Outlet } from "react-router-dom";

/** Lecturer layout — navigation sidebar + content area. */
export function LecturerLayout() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* TODO: Add lecturer navigation sidebar in feature/ui-lecturer-layout */}
      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <h1 className="text-lg font-semibold text-gray-900">CaseTree AI — Lecturer</h1>
      </header>
      <main className="max-w-7xl mx-auto px-6 py-8">
        <Outlet />
      </main>
    </div>
  );
}
