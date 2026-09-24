# CaseTree AI — Website & Application Architecture Reference

> **Target Platform**: Google Stitch UI Generation  
> **Product Name**: CaseTree AI  
> **Full Title**: CaseTree AI — AI Platform for Interactive Branching Case Studies and Open Review in University Teaching  
> **Repository**: https://github.com/HoangNam2464/CaseTree-AI

---

## 1. Product Vision

CaseTree AI is an educational technology platform engineered specifically for **university-level teaching and learning**. It transforms static teaching materials (textbooks, lecture slides, academic papers, and syllabi) into rich, interactive **Branching Study** and **Review Study** cases.

Rather than passively reading theoretical texts, students are immersed into realistic professional dilemmas where each decision reveals lecturer-authored/approved consequences and advances along predefined branches into subsequent scenarios. Built-in **AI Reasoning / Challenge Support** poses targeted challenge/counter-questions to challenge student reasoning without grading, scoring, or determining academic pass/fail.

Lecturers remain strictly in the loop: every AI-generated case starts in `DRAFT` status and must be verified, edited, approved, and explicitly published by the lecturer before any student can access it.

---

## 2. Target Users & Roles

The system strictly serves two distinct academic user roles:

| User Role | Responsibilities & Activities | Core Needs in UI |
|---|---|---|
| **Lecturer (`LECTURER`)** | Manages courses, uploads teaching materials (PDF/DOCX), triggers AI case generation, reviews and edits decision trees via interactive visual editor (ReactFlow), approves/publishes cases, inspects student branch choices, reasoning, and statistics, provides academic feedback. | Powerful, uncluttered management tools, visual tree editors, fast document ingestion, clear publication controls. |
| **Student (`STUDENT`)** | Participates in Branching Study (navigates decision points, observes consequences, articulates Student Reasoning per attempt, retries to explore alternative paths) and Review Study (analyzes case context and problems, submits proposed solutions and reasoning); engages in optional AI Reasoning / Challenge Support (up to 2 rounds of challenge-question interaction); writes post-case reflections. | Immersive reading experience, distraction-free decision interfaces, clear consequence feedback, intuitive challenge-question interaction panels. |

*(Note: Generic public visitors only have access to authentication screens `/login` and `/register`).*

---

## 3. Product Goals

1. **Active Decision-Making Over Passive Reading**: Elevate university case method pedagogy through dynamic multi-branch decision trees.
2. **AI with Human-in-the-Loop Governance**: AI drafts cases from authenticated course materials via RAG; the lecturer retains 100% editorial authority.
3. **Socratic Reasoning Challenge, NOT Autonomous Grading**: AI Reasoning / Challenge Support challenges student reasoning with targeted counter-questions capped at 2 rounds; evaluation remains the exclusive domain of faculty.
4. **Pedagogical Insights**: Provide lecturers with simple, clear learning-flow statistics (branch selection distribution, completion rates, attempt counts, and outcomes) to observe student decision pathways.

---

## 4. Product Experience Attributes

- **Academic & Focused**: Designed for critical thinking, free of gamified badges or childish icons.
- **Efficient & Professional**: Dense, well-spaced information architecture suitable for desktop monitors and lecture hall workstations.
- **Predictable & Governed**: Transparent AI provenance showing which teaching materials informed each case dilemma.
- **Light-First Academic Presentation**: Clean, neutral, high-contrast light surfaces emphasizing clear readability, a calm academic interface, professional presentation, and content-first design suitable for analytical reading and review sessions.

---

## 5. Actual Application Sitemap

Based on the verified routing architecture (`frontend/src/app/router.tsx`):

### 5.1. Public Routes
- `/login` — Sign in with university credentials and role selector.
- `/register` — Account registration.

### 5.2. Lecturer Portal (`/lecturer`)
- `/lecturer/courses` — Course catalog & creation interface.
- `/lecturer/courses/:courseId/materials` — Teaching materials upload center (PDF, DOCX parsing and RAG chunk status).
- `/lecturer/courses/:courseId/cases` — Case study management, filter by learning mode (`BRANCHING_STUDY` vs `REVIEW_STUDY`), trigger AI Case Generation.
- `/lecturer/cases/:caseId/review` — Interactive ReactFlow Decision Tree Editor, node editing, dilemma option authoring, approval and publishing workflow.
- `/lecturer/cases/:caseId/feedback` — Review student reasoning/submissions and submit qualitative lecturer feedback.
- `/lecturer/statistics` — Branch selection distribution, participation metrics, and attempt analytics.

### 5.3. Student Portal (`/student`)
- `/student/cases/:caseId/branching-play` — Branching Case Player (Situation → Dilemma Options → Consequence → Next Node).
- `/student/cases/:caseId/attempt/:attemptId/reflect` — Post-attempt reflection prompt and justification submission.
- `/student/cases/:caseId/challenge/:sessionId` — AI Reasoning / Challenge Support interface (1–2 rounds of targeted challenge/counter-questions).
- `/student/cases/:caseId/review-study` — Review Study case analysis, proposed solution formulation, and reasoning submission.
- `/student/cases/:caseId/review-study/:submissionId/feedback` — Inspection of lecturer feedback on review study.

---

## 6. Major Application Workflows

```
Workflow 1: Material Ingestion
Lecturer uploads PDF/DOCX → MinIO Storage → FastAPI parses & chunks → pgvector embeddings stored.

Workflow 2: AI Case Generation & Specification
Teaching material / lecturer-provided case context → RAG retrieves course chunks → LLM drafts Case JSON (Branching Study or Review Study) → Case created as DRAFT.

Workflow 3: Human-in-the-Loop Review
Lecturer verifies and edits case draft → Validates Branching Study tree structure (no cycles, reachable nodes, valid terminal nodes) or Review Study content → Moves through REVIEWED → APPROVED → PUBLISHED.

Workflow 4: Branching Study
Context/Data → Decision Point → Select Option → Student Reasoning per Attempt → Lecturer-authored/approved Consequence → Next Node → Outcome → Student Reflection → New Attempt / Retry.

Workflow 5: Review Study
Context/Data → Problem → Student Analysis → Proposed Solution → Student Reasoning → Lecturer Review / Feedback → Student Reflection.

Workflow 6: AI Reasoning / Challenge Support
Student submits reasoning (Branching Study or Review Study) → Optional Challenge Support invoked → AI poses targeted challenge/counter-question (Round 1) → Student may clarify/respond (Round 2 max) → Challenge concluded.
(Strict guardrails: cross-mode support for both Branching and Review Study, maximum 2 rounds, challenge/counter-questions only, no grading, no scoring, no academic right/wrong decision).
```

---

## 7. Internal Design Tooling ("Bắt đầu với thiết kế của bạn")

> **Classification: INTERNAL DESIGN TOOLING**  
> This tooling is strictly used for Stitch/UI-authoring workflows during development. It is **NOT** a CaseTree AI user-facing product feature, is **NOT** part of the Lecturer or Student product sitemap, and must **NOT** be treated as a product requirement.

- **Screen / Component Name**: `StartDesignModal` / `StartDesignPage` ("Bắt đầu với thiết kế của bạn").
- **Tooling Context**: Used internally by designers and developers during prototyping to provide design references and context:
  1. Pasting a standard `DESIGN.md` markdown specification.
  2. Dragging and dropping design files, code assets, brand logos, fonts, or Figma `.fig` project files.
  3. Supplying a public GitHub repository URL for direct code/architecture inspection.
  4. Supplying a live website URL for visual and contextual reference.
  5. Providing specific additional natural-language prompts and instructions.
- **Tooling Outcome**: Consolidates design inputs into a structured payload for Stitch UI generation; strictly excluded from CaseTree AI runtime product workflows.

---

## 8. Design Roadmap

Prioritized according to the confirmed product screen sequencing in `CaseTree-AI_UX-Redesign_Discovery-Plan.md` (Sections D & P.3):

### 8.1. Immediate Implementation (NOW)
- **P0 — Global Foundation**: App shell, role-aware navigation (Lecturer & Student layouts), authentication screens (`/login`, `/register`), case status indicators, and foundational design system components under the approved light-first palette.
- **P1 — Core Lecturer Flow**: Course catalog (`/lecturer/courses`), materials ingestion management (`/lecturer/courses/:courseId/materials`), case list (`/lecturer/courses/:courseId/cases`), and interactive Case Review with ReactFlow Decision Tree Editor (`/lecturer/cases/:caseId/review`).
- **P2 — Core Student Flow**: Branching Case Player (`/student/cases/:caseId/branching-play`), post-outcome reflection (`/student/cases/:caseId/attempt/:attemptId/reflect`), and cross-mode AI Reasoning / Challenge Support (`/student/cases/:caseId/challenge/:sessionId`).

### 8.2. Secondary Implementation (LATER)
- **P3 — Support & Statistics**: Basic Learning-Flow Statistics (`/lecturer/statistics`) and Lecturer Review/Feedback interface for student submissions (`/lecturer/cases/:caseId/feedback`).
- **P4 — Secondary Review Study**: Review Study reading & solution formulation (`/student/cases/:caseId/review-study`) and student inspection of lecturer feedback (`/student/cases/:caseId/review-study/:submissionId/feedback`).

*(Note: Internal design tooling such as the Start Design modal is categorized as NOT NEEDED YET / tooling-only and is excluded from the product design roadmap).*
