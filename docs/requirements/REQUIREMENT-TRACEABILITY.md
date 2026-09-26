# Edu-Branch-AI — Proposal Requirement Traceability Matrix

> **Authoritative Source**: `C1SE_65-CaseTree-AI-Proposal_V1_1.docx` (September 21, 2026 — Updated to Edu-Branch-AI: two learning modes)  
> **Mandatory Status States**:
> - **`Documented`**: Specification authored in `docs/` according to standard; no code skeleton exists.
> - **`Structurally Scaffolded`**: Specification documented AND non-business architectural skeleton exists (entity placeholders, DTO records, routing shell, health checks).
> - **`Implemented`**: Production business logic and workflow active (**Strictly ZERO in this migration phase**).

---

## 1. Traceability Matrix: Core Traceability Items Extracted from Proposal V1.1

| # | Traceability Item | Proposal Source Reference | Authoritative Documentation | Target Implementation Area | Status |
| :-: | :--- | :--- | :--- | :--- | :--- |
| **1** | **Authentication & Roles** | Section 4 & Section 6 | [`docs/features/FEATURE-AUTH-AND-ROLES.md`](../features/FEATURE-AUTH-AND-ROLES.md) | Backend `auth/`, `user/` + Frontend `types/index.ts` | **Structurally Scaffolded** |
| **2** | **Lecturer Role** | Section 2 & Section 4 | [`docs/features/FEATURE-AUTH-AND-ROLES.md`](../features/FEATURE-AUTH-AND-ROLES.md) | Backend `user/`, Frontend `layouts/LecturerLayout.tsx` | **Structurally Scaffolded** |
| **3** | **Student Role** | Section 2 & Section 4 | [`docs/features/FEATURE-AUTH-AND-ROLES.md`](../features/FEATURE-AUTH-AND-ROLES.md) | Backend `user/`, Frontend `layouts/StudentLayout.tsx` | **Structurally Scaffolded** |
| **4** | **Course Context** | Section 4 & Table 1 | [`docs/features/FEATURE-COURSE-AND-MATERIALS.md`](../features/FEATURE-COURSE-AND-MATERIALS.md) | Backend `course/` + Frontend `pages/lecturer/CoursesPage.tsx` | **Structurally Scaffolded** |
| **5** | **Teaching Materials (PDF/DOCX)** | Section 2 & Section 4 | [`docs/features/FEATURE-COURSE-AND-MATERIALS.md`](../features/FEATURE-COURSE-AND-MATERIALS.md) | Backend `material/` + MinIO Object Storage | **Structurally Scaffolded** |
| **6** | **Document Processing & Chunking** | Section 4 & Section 6 | [`docs/features/FEATURE-DOCUMENT-PROCESSING-AND-RAG.md`](../features/FEATURE-DOCUMENT-PROCESSING-AND-RAG.md) | AI Service `ingestion/` (parser + chunker) | **Structurally Scaffolded** |
| **7** | **RAG Retrieval (pgvector)** | Section 4 & Section 7 | [`docs/features/FEATURE-DOCUMENT-PROCESSING-AND-RAG.md`](../features/FEATURE-DOCUMENT-PROCESSING-AND-RAG.md) | AI Service `retrieval/` + pgvector HNSW | **Structurally Scaffolded** |
| **8** | **AI Case Draft Generation** | Section 4 & Section 6 | [`docs/features/FEATURE-CASE-GENERATION.md`](../features/FEATURE-CASE-GENERATION.md) | AI Service `generation/` (Structured Output) | **Structurally Scaffolded** |
| **9** | **Two Learning Modes** | Proposal line 34, 75 | [`docs/architecture/DATA-FLOW.md`](../architecture/DATA-FLOW.md) | Backend `cases.learning_mode`, Frontend types | **Structurally Scaffolded** |
| **10** | **Branching Decision Tree** | Section 2 & Section 4 | [`docs/features/FEATURE-DECISION-TREE.md`](../features/FEATURE-DECISION-TREE.md) | Backend `case/`, Frontend ReactFlow | **Structurally Scaffolded** |
| **11** | **Situation Node & Options** | Section 4 & Section 9 | [`docs/features/FEATURE-DECISION-TREE.md`](../features/FEATURE-DECISION-TREE.md) | Backend DB `case_nodes`, `case_options` | **Structurally Scaffolded** |
| **12** | **Consequences (Author/Approved)** | Section 4 & Section 9 | [`docs/features/FEATURE-DECISION-TREE.md`](../features/FEATURE-DECISION-TREE.md) | Backend `case_options.consequence` field | **Structurally Scaffolded** |
| **13** | **Lecturer Review & Edit** | Section 2 & Section 4 | [`docs/features/FEATURE-CASE-REVIEW-AND-PUBLISHING.md`](../features/FEATURE-CASE-REVIEW-AND-PUBLISHING.md) | Frontend `pages/lecturer/CaseReviewPage.tsx` | **Structurally Scaffolded** |
| **14** | **Lecturer Approval & Publishing** | Section 7 & Section 10 | [`docs/features/FEATURE-CASE-REVIEW-AND-PUBLISHING.md`](../features/FEATURE-CASE-REVIEW-AND-PUBLISHING.md) | Backend `CaseStatus` (APPROVED, PUBLISHED) | **Structurally Scaffolded** |
| **15** | **Branching Case Player** | Proposal line 35, 76 | [`docs/features/FEATURE-BRANCHING-STUDY.md`](../features/FEATURE-BRANCHING-STUDY.md) | Frontend `pages/student/BranchingCasePlayerPage.tsx` | **Structurally Scaffolded** |
| **16** | **Attempt & Retry Model** | Proposal line 35, 59, 76 | [`docs/features/FEATURE-BRANCHING-ATTEMPT.md`](../features/FEATURE-BRANCHING-ATTEMPT.md) | Backend `branching-attempt/` + DB `branching_attempts` | **Structurally Scaffolded** |
| **17** | **Reasoning per Attempt** | Proposal line 35, 59, 76 | [`docs/features/FEATURE-BRANCHING-STUDY.md`](../features/FEATURE-BRANCHING-STUDY.md) | Backend `reasoning/` + DB `student_reasoning` | **Structurally Scaffolded** |
| **18** | **Outcome & Student Reflection** | Proposal line 35, 60, 76 | [`docs/features/FEATURE-REFLECTION.md`](../features/FEATURE-REFLECTION.md) | Frontend `pages/student/ReflectionPage.tsx` | **Structurally Scaffolded** |
| **19** | **Review Study Mode** | Proposal line 37, 61, 77 | [`docs/features/FEATURE-REVIEW-STUDY.md`](../features/FEATURE-REVIEW-STUDY.md) | Backend `review-study/`, Frontend `ReviewStudyPage.tsx` | **Structurally Scaffolded** |
| **20** | **Review Submissions (1 per case)** | Proposal line 37, 77 | [`docs/features/FEATURE-REVIEW-STUDY.md`](../features/FEATURE-REVIEW-STUDY.md) | Backend DB `review_study_submissions` (UNIQUE) | **Structurally Scaffolded** |
| **21** | **Lecturer Review & Feedback** | Proposal line 37, 61, 77 | [`docs/features/FEATURE-LECTURER-FEEDBACK.md`](../features/FEATURE-LECTURER-FEEDBACK.md) | Backend `lecturer-feedback/`, DB `lecturer_feedback` | **Structurally Scaffolded** |
| **22** | **Reflection on Review Feedback** | Proposal line 37, 61, 77 | [`docs/features/FEATURE-REFLECTION.md`](../features/FEATURE-REFLECTION.md) | Frontend `pages/student/ReviewFeedbackPage.tsx` | **Structurally Scaffolded** |
| **23** | **AI Reasoning/Challenge Support** | Proposal line 40, 63, 78 | [`docs/features/FEATURE-AI-REASONING-CHALLENGE-SUPPORT.md`](../features/FEATURE-AI-REASONING-CHALLENGE-SUPPORT.md) | AI Service `challenge_support/`, Backend module | **Structurally Scaffolded** |
| **24** | **1–2 Challenge Rounds Max** | Proposal line 40, 63, 78 | [`docs/features/FEATURE-AI-REASONING-CHALLENGE-SUPPORT.md`](../features/FEATURE-AI-REASONING-CHALLENGE-SUPPORT.md) | Backend DB check constraint + AI Service schema | **Structurally Scaffolded** |
| **25** | **No AI Grading / No Pass-Fail** | Proposal line 40, 63, 78 | [`docs/features/FEATURE-AI-REASONING-CHALLENGE-SUPPORT.md`](../features/FEATURE-AI-REASONING-CHALLENGE-SUPPORT.md) | System Invariant INV-10 | **Structurally Scaffolded** |
| **26** | **Basic Learning-Flow Statistics** | Proposal line 65, 87 | [`docs/features/FEATURE-BASIC-STATISTICS.md`](../features/FEATURE-BASIC-STATISTICS.md) | Backend `statistics/`, Frontend `StatisticsPage.tsx` | **Structurally Scaffolded** |
| **27** | **Notification Extension Point** | Section 4 (p. 7) | [`docs/features/FEATURE-NOTIFICATIONS.md`](../features/FEATURE-NOTIFICATIONS.md) | Backend `notification/` placeholder | **Documented** |
| **28** | **Quantitative Evaluation (Case Quality)**| Section 4 & Section 6 | [`docs/features/FEATURE-EVALUATION-AND-RESEARCH.md`](../features/FEATURE-EVALUATION-AND-RESEARCH.md) | AI/Backend `evaluation/` (research rubric only) | **Documented** |
| **29** | **Research Data Collection** | Section 6 & Section 10 | [`docs/features/FEATURE-EVALUATION-AND-RESEARCH.md`](../features/FEATURE-EVALUATION-AND-RESEARCH.md) | Offline / Export boundary | **Documented** |
| **30** | **Research Dataset / Evaluation** | Section 6 & Section 10 | [`docs/features/FEATURE-EVALUATION-AND-RESEARCH.md`](../features/FEATURE-EVALUATION-AND-RESEARCH.md) | Offline / Research report boundary | **Documented** |

---

## 2. Summary of Implementation Status

- **`Documented`**: 4 items (Notifications, Quantitative Evaluation, Research Data Collection, Research Dataset).
- **`Structurally Scaffolded`**: 26 items (Non-business skeletons, domain entity definitions, routing placeholders, schema types).
- **`Implemented`**: **0 items** (Complies strictly with the absolute rule: no feature implementation in this migration phase).
