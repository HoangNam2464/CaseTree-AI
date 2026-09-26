/**
 * Edu-Branch-AI — Application Router
 * Source of Truth: Proposal V1.1 & Final Migration Plan Rev 2
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
import { LecturerFeedbackPage } from "../pages/lecturer/LecturerFeedbackPage";
import { BranchingCasePlayerPage } from "../pages/student/BranchingCasePlayerPage";
import { ChallengeSupportPage } from "../pages/student/ChallengeSupportPage";
import { ReflectionPage } from "../pages/student/ReflectionPage";
import { ReviewStudyPage } from "../pages/student/ReviewStudyPage";
import { ReviewFeedbackPage } from "../pages/student/ReviewFeedbackPage";
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
    element: (
      <PrivateRoute role="LECTURER">
        <LecturerLayout />
      </PrivateRoute>
    ),
    children: [
      { path: "courses", element: <CoursesPage /> },
      { path: "courses/:courseId/materials", element: <MaterialsPage /> },
      { path: "courses/:courseId/cases", element: <CasesPage /> },
      { path: "cases/:caseId/review", element: <CaseReviewPage /> },
      { path: "cases/:caseId/feedback", element: <LecturerFeedbackPage /> },
      { path: "statistics", element: <StatisticsPage /> },
    ],
  },
  {
    path: "/student",
    element: (
      <PrivateRoute role="STUDENT">
        <StudentLayout />
      </PrivateRoute>
    ),
    children: [
      { path: "cases/:caseId/branching-play", element: <BranchingCasePlayerPage /> },
      { path: "cases/:caseId/attempt/:attemptId/reflect", element: <ReflectionPage /> },
      { path: "cases/:caseId/review-study", element: <ReviewStudyPage /> },
      { path: "cases/:caseId/review-study/:submissionId/feedback", element: <ReviewFeedbackPage /> },
      { path: "cases/:caseId/challenge/:sessionId", element: <ChallengeSupportPage /> },
    ],
  },
]);
