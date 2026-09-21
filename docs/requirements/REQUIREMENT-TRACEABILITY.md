# CaseTree AI — Proposal Requirement Traceability Matrix

> **Authoritative Source**: `C1SE_65-CaseTree-AI-Proposal_V1.0(5).docx` (International School, Duy Tan University — Capstone 1, 2026)  
> **Mandatory Status States**:
> - **`Documented`**: Specification authored in `docs/` according to the 15-section standard; no code skeleton exists.
> - **`Structurally Scaffolded`**: Specification documented AND non-business architectural skeleton exists (entity placeholders, DTO records, routing shell, health checks).
> - **`Implemented`**: Production business logic and workflow active (**Strictly ZERO in this task**).

---

## 1. Traceability Matrix: 30 Traceability Items Extracted from the Proposal

| # | Traceability Item | Proposal Source Section | Authoritative Documentation | Future Implementation Area | Status |
| :-: | :--- | :--- | :--- | :--- | :--- |
| **1** | **Account / Authentication / Roles** | Section 4 (p. 7) & Section 6 (p. 10) | [`docs/features/FEATURE-AUTH-AND-ROLES.md`](../features/FEATURE-AUTH-AND-ROLES.md) | Backend `auth/`, `user/` + Frontend `features/auth/` | **Structurally Scaffolded** |
| **2** | **Lecturer Role** | Section 2 (p. 6), Section 4 (p. 7) | [`docs/features/FEATURE-AUTH-AND-ROLES.md`](../features/FEATURE-AUTH-AND-ROLES.md) | Backend `user/entity/Role.java` | **Structurally Scaffolded** |
| **3** | **Student Role** | Section 2 (p. 6), Section 4 (p. 7) | [`docs/features/FEATURE-AUTH-AND-ROLES.md`](../features/FEATURE-AUTH-AND-ROLES.md) | Backend `user/entity/Role.java` | **Structurally Scaffolded** |
| **4** | **Course Context** | Section 4 (p. 7), Table 1 (p. 9) | [`docs/features/FEATURE-COURSE-AND-MATERIALS.md`](../features/FEATURE-COURSE-AND-MATERIALS.md) | Backend `course/` + Frontend `features/courses/` | **Structurally Scaffolded** |
| **5** | **Teaching Material** | Section 2 (p. 6), Section 4 (p. 7) | [`docs/features/FEATURE-COURSE-AND-MATERIALS.md`](../features/FEATURE-COURSE-AND-MATERIALS.md) | Backend `material/` + MinIO Object Storage | **Structurally Scaffolded** |
| **6** | **PDF / DOCX Formats** | Section 4 (p. 7) | [`docs/features/FEATURE-COURSE-AND-MATERIALS.md`](../features/FEATURE-COURSE-AND-MATERIALS.md) | AI Service `ingestion/parser.py` | **Structurally Scaffolded** |
| **7** | **Document Processing** | Section 4 (p. 7), Section 6 (p. 10) | [`docs/features/FEATURE-DOCUMENT-PROCESSING-AND-RAG.md`](../features/FEATURE-DOCUMENT-PROCESSING-AND-RAG.md) | AI Service `ingestion/` (chunker + parser) | **Structurally Scaffolded** |
| **8** | **RAG Retrieval** | Section 4 (p. 7), Section 7 (p. 11) | [`docs/features/FEATURE-DOCUMENT-PROCESSING-AND-RAG.md`](../features/FEATURE-DOCUMENT-PROCESSING-AND-RAG.md) | AI Service `retrieval/` + pgvector HNSW | **Structurally Scaffolded** |
| **9** | **AI Case Generator** | Section 4 (p. 7), Section 6 (p. 10) | [`docs/features/FEATURE-CASE-GENERATION.md`](../features/FEATURE-CASE-GENERATION.md) | AI Service `generation/case_generator/` | **Structurally Scaffolded** |
| **10** | **Structured JSON Output** | Section 4 (p. 7), Section 6 (p. 10) | [`docs/features/FEATURE-CASE-GENERATION.md`](../features/FEATURE-CASE-GENERATION.md) | AI Service `generation/schemas/` | **Structurally Scaffolded** |
| **11** | **JSON Schema Validation** | Section 4 (p. 7), Section 10 (p. 14) | [`docs/features/FEATURE-CASE-GENERATION.md`](../features/FEATURE-CASE-GENERATION.md) | AI Service Pydantic v2 validation | **Structurally Scaffolded** |
| **12** | **Branching Decision Tree** | Section 2 (p. 6), Section 4 (p. 7) | [`docs/features/FEATURE-DECISION-TREE.md`](../features/FEATURE-DECISION-TREE.md) | Backend `case/`, Frontend `components/tree/` | **Structurally Scaffolded** |
| **13** | **Situation (Node)** | Section 4 (p. 7), Section 9 (p. 13) | [`docs/features/FEATURE-DECISION-TREE.md`](../features/FEATURE-DECISION-TREE.md) | Backend `CaseNode.java`, DB `case_nodes` | **Structurally Scaffolded** |
| **14** | **Options (Choice)** | Section 4 (p. 7), Section 9 (p. 13) | [`docs/features/FEATURE-DECISION-TREE.md`](../features/FEATURE-DECISION-TREE.md) | Backend `CaseOption.java`, DB `case_options` | **Structurally Scaffolded** |
| **15** | **Consequences (Outcome)** | Section 4 (p. 7), Section 9 (p. 13) | [`docs/features/FEATURE-DECISION-TREE.md`](../features/FEATURE-DECISION-TREE.md) | Backend `CaseOption.consequence` field | **Structurally Scaffolded** |
| **16** | **Next Node (Edge)** | Section 4 (p. 7), Section 9 (p. 13) | [`docs/features/FEATURE-DECISION-TREE.md`](../features/FEATURE-DECISION-TREE.md) | Backend `CaseOption.next_node_id` field | **Structurally Scaffolded** |
| **17** | **Lecturer Review / Edit** | Section 2 (p. 6), Section 4 (p. 7) | [`docs/features/FEATURE-CASE-REVIEW-AND-PUBLISHING.md`](../features/FEATURE-CASE-REVIEW-AND-PUBLISHING.md) | Frontend `pages/lecturer/CaseReviewPage.tsx` | **Structurally Scaffolded** |
| **18** | **Lecturer Approval** | Section 7 (p. 11), Section 10 (p. 14) | [`docs/features/FEATURE-CASE-REVIEW-AND-PUBLISHING.md`](../features/FEATURE-CASE-REVIEW-AND-PUBLISHING.md) | Backend `CaseStatus.APPROVED` | **Structurally Scaffolded** |
| **19** | **Publishing** | Section 4 (p. 7), Section 7 (p. 11) | [`docs/features/FEATURE-CASE-REVIEW-AND-PUBLISHING.md`](../features/FEATURE-CASE-REVIEW-AND-PUBLISHING.md) | Backend `CaseStatus.PUBLISHED` | **Structurally Scaffolded** |
| **20** | **Interactive Case Simulator** | Section 2 (p. 6), Section 4 (p. 7) | [`docs/features/FEATURE-CASE-SIMULATOR-AND-ARGUMENT.md`](../features/FEATURE-CASE-SIMULATOR-AND-ARGUMENT.md) | Frontend `pages/student/SimulatorPage.tsx` | **Structurally Scaffolded** |
| **21** | **Student Decision** | Section 4 (p. 7), Section 6 (p. 10) | [`docs/features/FEATURE-CASE-SIMULATOR-AND-ARGUMENT.md`](../features/FEATURE-CASE-SIMULATOR-AND-ARGUMENT.md) | Backend `simulation/` + DB `simulation_sessions` | **Structurally Scaffolded** |
| **22** | **Immediate Consequence** | Section 2 (p. 6), Section 4 (p. 7) | [`docs/features/FEATURE-CASE-SIMULATOR-AND-ARGUMENT.md`](../features/FEATURE-CASE-SIMULATOR-AND-ARGUMENT.md) | Frontend `SimulatorPage` modal / panel | **Structurally Scaffolded** |
| **23** | **Student Justification / Argument** | Section 2 (p. 6), Section 4 (p. 7) | [`docs/features/FEATURE-CASE-SIMULATOR-AND-ARGUMENT.md`](../features/FEATURE-CASE-SIMULATOR-AND-ARGUMENT.md) | Backend `StudentArgument.java`, DB table | **Structurally Scaffolded** |
| **24** | **AI Debate Assistant (Devil's Advocate)** | Section 2 (p. 6), Section 4 (p. 7) | [`docs/features/FEATURE-DEBATE-ASSISTANT.md`](../features/FEATURE-DEBATE-ASSISTANT.md) | AI Service `debate/assistant/` | **Structurally Scaffolded** |
| **25** | **1–2 Debate Rounds Max** | Section 4 (p. 7), Section 7 (p. 11) | [`docs/features/FEATURE-DEBATE-ASSISTANT.md`](../features/FEATURE-DEBATE-ASSISTANT.md) | Backend `debate/` + AI Service validator | **Structurally Scaffolded** |
| **26** | **Lecturer Statistics** | Section 2 (p. 6), Section 4 (p. 7) | [`docs/features/FEATURE-LECTURER-STATISTICS.md`](../features/FEATURE-LECTURER-STATISTICS.md) | Backend `statistics/` + Frontend `StatisticsPage` | **Structurally Scaffolded** |
| **27** | **Notification** | Section 4 (p. 7) | [`docs/features/FEATURE-NOTIFICATIONS.md`](../features/FEATURE-NOTIFICATIONS.md) | Backend `notification/` placeholder | **Documented** |
| **28** | **Quantitative Evaluation** | Section 4 (p. 7), Section 6 (p. 10) | [`docs/features/FEATURE-EVALUATION-AND-RESEARCH.md`](../features/FEATURE-EVALUATION-AND-RESEARCH.md) | Backend `evaluation/` placeholder | **Documented** |
| **29** | **Research Data Collection** | Section 6 (p. 10), Section 10 (p. 14) | [`docs/features/FEATURE-EVALUATION-AND-RESEARCH.md`](../features/FEATURE-EVALUATION-AND-RESEARCH.md) | Offline / Export boundary | **Documented** |
| **30** | **Research Dataset / Evaluation** | Section 6 (p. 10), Section 10 (p. 14) | [`docs/features/FEATURE-EVALUATION-AND-RESEARCH.md`](../features/FEATURE-EVALUATION-AND-RESEARCH.md) | Offline / Research report boundary | **Documented** |

---

## 2. Summary of Implementation Status

- **`Documented`**: 4 items (Notifications, Quantitative Evaluation, Research Data Collection, Research Dataset).
- **`Structurally Scaffolded`**: 26 items (Non-business skeletons, domain entity definitions, routing placeholders, schema types).
- **`Implemented`**: **0 items** (Complies strictly with the absolute rule: no feature implementation in this task).
