/**
 * CaseTree AI — Application Router
 */

import { createBrowserRouter } from "react-router-dom";
import { PublicLayout } from "../layouts/PublicLayout";
import { LecturerLayout } from "../layouts/LecturerLayout";
import { StudentLayout } from "../layouts/StudentLayout";
import { LoginPage } from "../pages/LoginPage";
import { RegisterPage } from "../pages/RegisterPage";
import { CoursesPage } from "../pages/lecturer/CoursesPage";
import { MaterialsPage } from "../pages/lecturer/MaterialsPage";
import { CasesPage } from "../pages/lecturer/CasesPage";
import { CaseReviewPage } from "../pages/lecturer/CaseReviewPage";
import { StatisticsPage } from "../pages/lecturer/StatisticsPage";
import { SimulatorPage } from "../pages/student/SimulatorPage";
import { DebatePage } from "../pages/student/DebatePage";
import { PrivateRoute } from "../components/ui/PrivateRoute";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <PublicLayout />,
    children: [
      { index: true, element: <LoginPage /> },
      { path: "login", element: <LoginPage /> },
      { path: "register", element: <RegisterPage /> },
    ],
  },
  {
    path: "/lecturer",
    element: <PrivateRoute role="LECTURER"><LecturerLayout /></PrivateRoute>,
    children: [
      { path: "courses", element: <CoursesPage /> },
      { path: "courses/:courseId/materials", element: <MaterialsPage /> },
      { path: "courses/:courseId/cases", element: <CasesPage /> },
      { path: "cases/:caseId/review", element: <CaseReviewPage /> },
      { path: "statistics", element: <StatisticsPage /> },
    ],
  },
  {
    path: "/student",
    element: <PrivateRoute role="STUDENT"><StudentLayout /></PrivateRoute>,
    children: [
      { path: "cases/:caseId/simulate", element: <SimulatorPage /> },
      { path: "cases/:caseId/debate/:sessionId", element: <DebatePage /> },
    ],
  },
]);
