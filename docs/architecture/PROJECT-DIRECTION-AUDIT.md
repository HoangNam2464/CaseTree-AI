# Edu-Branch-AI — Project Direction Audit

> **Audit Type**: Read-Only Source-of-Truth & Architectural Direction Audit  
> **Target System**: Edu-Branch-AI (`https://github.com/HoangNam2464/CaseTree-AI`)  
> **Primary Benchmark (Priority 1)**: `C1SE_65-CaseTree-AI-Proposal_V1.0.docx`  
> **Project Owner Decisions (Priority 2)**: 3-tier boundary (Frontend → Backend → AI Service), PostgreSQL+pgvector, Redis, MinIO, separate internal AI service, skeleton/docs only.  
> **Engineering Reference (Priority 4)**: `ai-teacher-copilot` (`D:\DU_AN_2026\Python\ai-teacher-copilot`)  
> **Audit Date**: 2026-09-11  
> **Overall Verdict**: **YELLOW** (Project is generally well-aligned with core pedagogical workflows, but inherits technical assumptions and governance rule contradictions from the reference repository that require formal Owner resolution).

---

## 1. Executive Summary

### "Is the current project going in the correct direction?"

**Yes, conceptually and functionally, but with technical inheritance debt.**

- **Pedagogical & Functional Direction**: **GREEN**. The repository faithfully represents the core pedagogical workflow mandated by the Proposal: university course context → teaching material upload (PDF/DOCX) → RAG semantic retrieval → AI-generated branching decision tree (JSON Schema) → mandatory human-in-the-loop review & approval → publishing → interactive case simulator → decision consequence reveal → student argument capture → AI Debate Assistant (Devil's Advocate, 1–2 rounds max, no grading) → lecturer statistics → quantitative evaluation research boundary.
- **Reference Leakage Protection**: **GREEN**. All product-specific K-12 features from `ai-teacher-copilot` (Lesson Planner, Exam/Quiz Generator, Teacher Personal Workspace, Word Export, Bloom's Taxonomy, Autonomous Grading) have been cleanly excluded from both documentation and skeleton code.
- **Service Boundaries & AI Governance**: **GREEN**. The strict 3-tier hierarchy (`Frontend → Backend Gateway → FastAPI AI Service (Internal Only)`) and AI safety rules (untrusted material wrapped in `<sources>`, 2-round cap, zero autonomous grading) are documented with high fidelity.
- **Technology & Rule Alignment**: **YELLOW**. The project inherited Spring Boot 3 (Java 17) directly from `ai-teacher-copilot` during initial scaffolding. While documentation in `ADR-001-TECHNOLOGY-STACK.md` now treats Backend Gateway as a Candidate Option, **all 14 `.agents/rules/*.md` files still hardcode Spring Boot as an immutable project rule**, conflicting with both the Proposal (which specifies Node.js/NestJS or Python FastAPI) and the Project Owner's explicit candidate-option stance. Furthermore, `package.json` installed React 19 and TailwindCSS v4 despite rules prescribing React 18 and TailwindCSS v3.

---

## 2. What the Proposal Actually Defines

Extracted directly from `C1SE_65-CaseTree-AI-Proposal_V1.0.docx`:

- **Full Project Identity**: *"Edu-Branch-AI — AI Platform for Interactive Branching Case Studies and Open Review in University Teaching"* (Acronym: EBA, Lead: International School, Duy Tan University, Capstone 1, 2026).
- **Target Audience & Actors**:
  - Higher education / university teaching (Business, Law, Medicine, IT, Engineering).
  - Primary Actors: **Lecturer** and **Student**.
- **Core Problems Addressed**:
  1. Static, linear case studies in course materials prevent students from experiencing multi-directional consequences of decisions.
  2. Heavy authoring burden on lecturers to write and update realistic case scenarios aligned with weekly syllabi.
  3. Lack of critical-thinking challenge: student submissions are rarely debated in real-time.
  4. Market gap: Existing tools (H5P, BranchTrack, Kritik) do not combine AI case generation bound to a lecturer's own materials with a real-time AI debate partner.
- **Proposed Solution**:
  - Web platform integrating a RAG-based AI Case Generator with an AI Debate Assistant.
  - Course context and teaching material upload (PDF / DOCX).
  - Branching Decision Tree case studies modeled as: **`Situation → Options → Consequences → Next Node`**.
  - Form/list editor for lecturer review, edit, and approval before publishing (human-in-the-loop).
  - Interactive Case Simulator with immediate consequence reveal and short argument capture.
  - AI Debate Assistant acting as a **Devil's Advocate** (1–2 rounds of targeted counter-questions).
  - Simple lecturer statistics on branch choices and argument quality.
  - Quantitative evaluation module supporting the confirmed research question.
  - Deadline notification reminders (email / in-app).
- **Confirmed Research Question**:
  > *"Evaluate the quality of AI-generated cases (produced from a lecturer's teaching material via RAG) compared with lecturer-authored cases, based on a rubric covering realism, difficulty, and alignment with the course content."*
- **Technology Options Permitted by Proposal**:
  - Frontend: React.js / Next.js, TailwindCSS.
  - Graph/Tree Visualization: ReactFlow or jsPlumb.
  - Backend: **Node.js (NestJS/Express)** OR **Python FastAPI**. *(Spring Boot is referenced in Table 5 external links, but not listed in Section 7 or Section 11 stack)*.
  - Database & Cache: PostgreSQL (or MongoDB), Redis.
  - AI/LLM: OpenAI GPT-4o-mini / Gemini Flash API + LangChain.
- **Key Constraints & Ethics**:
  - AI Debate Assistant **must avoid making final pass/fail or academic-integrity judgments**; challenges reasoning but does not assign grades.
  - Economic: Total project budget cannot exceed $4,700. Capping debate rounds to 1–2 controls API cost.
  - Human-in-the-loop: Every case must be approved by the lecturer before publication.

---

## 3. Current Repository Reality

The current repository reflects the state after bootstrap scaffolding and documentation alignment:

- **Root Structure**: Complete repository foundation with `.env.example`, `docker-compose.yml`, `CONTRIBUTING.md`, `SECURITY.md`, `README.md`, `CHANGELOG.md`, `CODE_OF_CONDUCT.md`.
- **Backend (`backend/`)**:
  - Scaffolded as Spring Boot 3.3.4 (Java 17) Maven project (`pom.xml`).
  - Contains JPA entities for all domain models: `User`, `Role`, `Course`, `TeachingMaterial`, `ProcessingStatus`, `Case`, `CaseNode`, `CaseOption`, `CaseStatus`, `SimulationSession`, `StudentArgument`, `DebateSession`, `DebateMessage`, `MessageRole`.
  - Flyway migration `V1__init_schema.sql` establishes 10 core tables + pgvector extensions.
  - Health endpoint `HealthController.java` (`/api/v1/health`) is active.
  - **Zero business services, controllers, or repositories implemented.**
- **AI Service (`ai-service/`)**:
  - Scaffolded as Python 3.12 + FastAPI project (`requirements.txt`).
  - Provider abstraction interfaces (`base.py`, `factory.py`, `gemini_provider.py`, `openai_provider.py`).
  - Pydantic v2 schemas (`decision_tree.py`, `requests.py`) with BFS DAG cycle detection.
  - Ingestion stubs (`parser.py`, `chunker.py`) with LangChain text splitters.
  - Health endpoint `/health` is active in `main.py`. Route routers are commented out as placeholders.
  - **Zero RAG execution, zero active LLM calls, zero business routes active.**
- **Frontend (`frontend/`)**:
  - Scaffolded as Vite + React application with TypeScript.
  - Contains route definitions in `router.tsx` mirroring the Proposal workflow (`/lecturer/courses`, `/lecturer/courses/:courseId/cases`, `/lecturer/cases/:caseId/review`, `/student/cases/:caseId/simulate`, `/student/cases/:caseId/debate/:sessionId`).
  - Layouts (`LecturerLayout`, `StudentLayout`, `PublicLayout`) and placeholder view pages exist.
  - Dependencies in `package.json`: `react: ^19.2.8`, `tailwindcss: ^4.3.3`, `reactflow: ^11.11.4`, `zustand: ^5.0.15`, `axios: ^1.20.0`.
  - **Zero production feature screens or mock workflows active.**
- **Infrastructure (`infrastructure/`)**:
  - `docker-compose.yml` configures PostgreSQL 16 + pgvector (`5432`), Redis 7 (`6379`), and MinIO (`9000`/`9001`).
  - PostgreSQL init script enables `vector` and `uuid-ossp` extensions.
- **Documentation (`docs/`)**:
  - 11 feature specifications in `docs/features/` covering all 30 traceability items.
  - `ADR-001-TECHNOLOGY-STACK.md`, `SERVICE-BOUNDARIES.md`, `DATA-FLOW.md`, `DECISION-TREE-MODEL.md`, `REFERENCE-REPOSITORY-AUDIT.md`, `REQUIREMENT-TRACEABILITY.md`, `BOOTSTRAP-AUDIT.md`.
- **Governance (`.agents/rules/`, `.github/`)**:
  - 14 rule files in `.agents/rules/` and `copilot-instructions.md` in `.github/`.

---

## 4. Proposal vs Current Repository Matrix

| Area | Proposal Specification | Current Repository Reality | Alignment | Issue / Discrepancy |
| :--- | :--- | :--- | :---: | :--- |
| **Product Purpose** | Branching case studies + AI debate for university education | Accurately documented in README, architecture, and feature specs | **Fully Aligned** | None. |
| **Target Actors** | Lecturer and Student | Entity `Role` (`LECTURER`, `STUDENT`), route guards, UI layouts | **Fully Aligned** | None. |
| **Course Context** | Course container bound to lecturer; materials belong to course | `Course` entity, `courses` table, `/lecturer/courses` UI shell | **Fully Aligned** | None. |
| **Teaching Materials** | PDF / DOCX upload stored for RAG processing | `TeachingMaterial` entity, MinIO object storage config | **Fully Aligned** | None. |
| **RAG Pipeline** | Parse → Chunk → Embed → pgvector → Context | `document_chunks` table, PyPDF/python-docx/LangChain stubs | **Fully Aligned** | LangChain must remain allowed option, not mandatory. |
| **Decision Tree Model** | Situation → Options → Consequences → Next Node | `CaseNode`, `CaseOption`, Pydantic tree schema, DAG cycle validator | **Fully Aligned** | None. |
| **Human-in-the-Loop** | Lecturer review & approval before publishing | `CaseStatus` state machine (`DRAFT→REVIEWED→APPROVED→PUBLISHED`) | **Fully Aligned** | None. |
| **Student Simulator** | Role-play decisions, immediate consequence, argument capture | `SimulationSession`, `StudentArgument`, simulator view shell | **Fully Aligned** | None. |
| **AI Debate Assistant** | Socratic Devil's Advocate, 1–2 rounds max, no grading | `DebateSession`, max 2 round schema checks, anti-grading rules | **Fully Aligned** | None. |
| **Lecturer Statistics** | Branch selection percentages & argument inspection | Statistics DTO schema, `/lecturer/statistics` view shell | **Fully Aligned** | None. |
| **Notifications** | Deadlines reminders: Email / In-App | Documented in `FEATURE-NOTIFICATIONS.md` as open options | **Fully Aligned** | Technology unselected pending Owner confirmation. |
| **Evaluation / Research** | AI vs human case quality rubric (realism, difficulty, alignment) | `EVALUATION-DESIGN.md`, `FEATURE-EVALUATION-AND-RESEARCH.md` | **Partially Aligned** | Implementation method marked "Open / To Be Decided". |
| **Backend Framework** | Node.js (NestJS/Express) OR Python FastAPI | Java 17 / Spring Boot 3 scaffolded | **Partially Aligned** | Inherited from reference repo; marked Candidate Option in ADR-001, but hardcoded in `.agents/rules/`. |
| **Frontend Stack** | React.js / Next.js + TailwindCSS | React 19 + TailwindCSS v4 + ReactFlow | **Partially Aligned** | Version drift: package.json has React 19 & Tailwind v4; rules say React 18 & Tailwind v3. |
| **Decision Tree Canvas** | ReactFlow or jsPlumb | ReactFlow 11.11.4 in package.json | **Fully Aligned** | Aligns with Proposal option. |

---

## 5. Scope Audit

### 5.1 Correct Scope
- The 11 core feature areas match the Proposal: Auth/Roles, Course/Materials, Document Processing/RAG, Case Generation, Decision Tree Model, Review/Publishing, Simulator/Argument, Debate Assistant, Lecturer Statistics, Notifications, Quantitative Research Evaluation.
- The 30 traceability items accurately reflect the functional and pedagogical touchpoints of the Proposal.

### 5.2 Missing Scope
- **None**. All Proposal capabilities are represented either as structural skeletons or formal documentation specifications.

### 5.3 Added Scope
- **None**. No extraneous business capabilities have been added.

### 5.4 Altered Scope
- **"Open Review" Terminology**: The Proposal title includes *"and Open Review"*, while Proposal Table 1 states that *"Peer / public review of student work"* is *"Planned (future work)"* and not in MVP. The current documentation correctly prioritizes the Lecturer Review workflow and treats open peer review as a post-MVP phase.

### 5.5 Inherited Scope from Reference Repository
- **Spring Boot 3 API Gateway Architecture**: The multi-package Java backend structure (`auth/`, `course/`, `material/`, `case_/`, `simulation/`, `debate/`, `statistics/`, `common/`) was directly cloned from the structural style of `ai-teacher-copilot/backend`.
- **Flyway Database Migration Pattern**: `V1__init_schema.sql` mirrors the migration pattern of `ai-teacher-copilot`.
- **MinIO S3 Integration Pattern**: Bucket structure and object key conventions were inherited from `ai-teacher-copilot`.

### 5.6 Unsupported Scope
- **None active**. All reference-specific K-12 modules were audited and blocked.

---

## 6. Architecture Audit

```
┌────────────────────────────────────────────────────────┐
│  Client Tier (Browser)                                 │
│  React + Vite + TypeScript + TailwindCSS + ReactFlow   │
└───────────────────────────┬────────────────────────────┘
                            │ HTTPS / REST API + JWT
                            ▼
┌────────────────────────────────────────────────────────┐
│  Backend Gateway (Candidate: Spring Boot / NestJS / FA)│
│  • Auth & User Management                               │
│  • Course & Material Metadata                           │
│  • Case Lifecycle & Persistence                         │
│  • Simulation Sessions & Argument Persistence           │
│  • Debate History Persistence & 2-Round Gate            │
│  • Lecturer Statistics Aggregations                     │
└────────────┬──────────────┬──────────────────┬─────────┘
             │ SQL / Flyway │ S3 API           │ Internal HTTP
             ▼              ▼                  ▼
┌──────────────────┐ ┌─────────────┐ ┌───────────────────────────┐
│ PostgreSQL 16    │ │ MinIO S3    │ │ FastAPI AI Service        │
│ + pgvector       │ │ (PDF/DOCX)  │ │ (INTERNAL ONLY)           │
│ (Metadata & DB)  │ └─────────────┘ │ • Document Parser/Chunker │
└──────────────────┘                 │ • pgvector Semantic Search│
┌──────────────────┐                 │ • Structured LLM Case Gen │
│ Redis 7 (Cache)  │                 │ • AI Debate Assistant     │
└──────────────────┘                 └─────────────┬─────────────┘
                                                   │ HTTPS
                                                   ▼
                                     ┌───────────────────────────┐
                                     │ LLM Providers             │
                                     │ Gemini 2.0 / GPT-4o-mini  │
                                     └───────────────────────────┘
```

- **Frontend**: Clean separation. Browser code talks exclusively to Backend Gateway via REST API; never calls the AI Service directly.
- **Backend Gateway**: Acts as the single external gateway, managing security, user identity, business state transitions, and database persistence.
- **AI Service**: Strictly internal microservice. Not exposed to public ingress; authenticated via `X-Internal-API-Key`. Owns parsing, chunking, embeddings, pgvector queries, LLM prompting, and schema validation.
- **PostgreSQL 16 + pgvector**: Unified storage engine for business relations and vector embeddings. High cohesion.
- **Redis 7**: Documented role for token blacklist and session caching.
- **MinIO**: S3-compatible local object storage for uploaded teaching materials.
- **Decision Tree Domain Model**: Relational database is correctly established as the absolute source of truth; visual canvas (ReactFlow) is strictly a presentation projection.

---

## 7. Technology Audit

| Technology | Current Role | Proposal / Owner Source | Classification | Concern / Status |
| :--- | :--- | :--- | :--- | :--- |
| **React** | Client UI framework | Proposal Section 7 & 11 | **`Proposal Requirement`** | Package has React 19 (`^19.2.8`); rules cite React 18. Minor version drift. |
| **TailwindCSS** | UI utility styling | Proposal Section 11 | **`Proposal Requirement`** | Package has Tailwind v4 (`^4.3.3`); UI rules cite Tailwind v3. Syntax divergence risk. |
| **ReactFlow** | Decision tree visualization | Proposal Section 11 | **`Proposal Requirement`** | Aligned (`^11.11.4`). Correctly isolated from domain truth. |
| **Spring Boot 3** | Backend Gateway skeleton | Reference repo / Table 5 link | **`Candidate Option`** | Inherited scaffold; conflicts with Proposal body (NestJS / FastAPI). Rules hardcode it. |
| **Node.js (NestJS)** | Candidate Backend | Proposal Section 7 & 11 | **`Candidate Option`** | Proposal-supported option; not currently scaffolded. |
| **FastAPI** | AI Service (and candidate backend) | Proposal Section 7 & Owner Decision | **`Owner Decision`** | Confirmed for AI Service; candidate for unified backend. |
| **PostgreSQL 16** | Relational database | Proposal Section 11 & Owner Decision | **`Proposal / Owner Decision`**| Fully aligned. |
| **pgvector** | Vector similarity extension | Owner Decision | **`Owner Decision`** | Confirmed for embedding storage. Fully aligned. |
| **Redis 7** | Cache / session store | Proposal Section 11 & Owner Decision | **`Proposal / Owner Decision`**| Fully aligned. |
| **MinIO** | Object storage (PDF/DOCX) | Owner Decision | **`Owner Decision`** | S3-compatible document storage. Fully aligned. |
| **Gemini 2.0 Flash** | Primary LLM provider | Proposal Section 6 & 11 | **`Proposal Requirement`** | Low-cost tier. Abstracted via provider interface. |
| **OpenAI GPT-4o-mini**| Fallback LLM provider | Proposal Section 6 & 11 | **`Proposal Requirement`** | Low-cost tier. Abstracted via provider interface. |
| **LangChain** | Chunking & RAG orchestration | Proposal Section 11 | **`Allowed Option`** | Documented as allowed/possible option; not mandatory architecture. |

---

## 8. Feature Documentation Audit

| Feature Area | Proposal Alignment | Documentation Quality | Inherited Content | Status |
| :--- | :---: | :---: | :---: | :---: |
| **1. Auth & Roles** | Fully Aligned | High (15 sections complete) | Generic JWT pattern adapted | `Structurally Scaffolded` |
| **2. Course & Materials** | Fully Aligned | High (15 sections complete) | MinIO S3 storage pattern adapted | `Structurally Scaffolded` |
| **3. Document Processing & RAG** | Fully Aligned | High (15 sections complete) | `<sources>` boundary from reference | `Structurally Scaffolded` |
| **4. Case Generation** | Fully Aligned | High (15 sections complete) | Pydantic JSON schema pattern adapted | `Structurally Scaffolded` |
| **5. Decision Tree Model** | Fully Aligned | High (15 sections complete) | Novel CaseTree domain model | `Structurally Scaffolded` |
| **6. Case Review & Publishing** | Fully Aligned | High (15 sections complete) | Novel human-in-the-loop workflow | `Structurally Scaffolded` |
| **7. Simulator & Argument** | Fully Aligned | High (15 sections complete) | Novel role-play & argument capture | `Structurally Scaffolded` |
| **8. Debate Assistant** | Fully Aligned | High (15 sections complete) | Novel Devil's Advocate Socratic rules | `Structurally Scaffolded` |
| **9. Lecturer Statistics** | Fully Aligned | High (15 sections complete) | Scoped to simple cohort stats | `Structurally Scaffolded` |
| **10. Notifications** | Fully Aligned | High (15 sections complete) | Kept strictly at Proposal options | `Documented` |
| **11. Evaluation & Research** | Fully Aligned | High (15 sections complete) | Rubric (realism, difficulty, alignment) | `Documented` |

---

## 9. Reference Repository Influence

### 9.1 Engineering Patterns Correctly Reused
- **Git Feature Branch Workflow**: `feature/<name> → develop → main` with Conventional Commits.
- **Service Isolation**: Clear network and token boundary between public backend and internal AI microservice.
- **Untrusted Prompt Boundary**: Encapsulating retrieved document chunks in `<sources>...</sources>` to prevent prompt injection.
- **Provider Abstraction Factory**: `providers/factory.py` preventing vendor SDK lock-in.
- **Flyway Database Migration Strategy**: Immutable, ordered versioning (`V1__init_schema.sql`).

### 9.2 Reference Patterns That Must Remain Reference-Only
- **K-12 Educational Workflows**: Lesson planning, syllabus drafting, and exam blueprints.
- **Bloom's Taxonomy Categorization**: Specific to K-12 test question generation.
- **Word/DOCX Export Engines**: Specific to lesson plan exporting.

### 9.3 Reference-Specific Business Concepts Leaked into Edu-Branch-AI
- **Finding**: Zero business logic leaks found in source code or feature documentation.
- **Minor Artifact**: In `frontend/src/layouts/LecturerLayout.tsx` line 3, a comment reads `/** Lecturer workspace layout — navigation sidebar + content area. */`. The term "workspace" was inherited colloquially from `ai-teacher-copilot`, though the layout itself is just a standard navigation shell.

---

## 10. Requirement Interpretation Issues & Classification

| Item | Location | Classification | Reason / Evidence | Severity |
| :--- | :--- | :---: | :--- | :---: |
| **Backend Framework in Rules** | `.agents/rules/*.md` (14 files) | **`CONFLICTING`** | `.agents/rules/` states Spring Boot is the mandatory stack, whereas Proposal specifies Node.js/FastAPI and ADR-001 marks it as a Candidate Option. | **High** |
| **React Version Drift** | `frontend/package.json` | **`INFERRED`** | Package has `react: ^19.2.8`, whereas rules and documentation specify `React 18`. | **Low** |
| **TailwindCSS Version Drift** | `frontend/package.json` | **`INFERRED`** | Package has `tailwindcss: ^4.3.3`, whereas `ui-design-standards.md` explicitly mandates `TailwindCSS v3`. | **Medium** |
| **"Open Review" Scope in MVP** | `docs/PROJECT_OVERVIEW.md` | **`INFERRED`** | Project title includes "Open Review", but Proposal Table 1 marks peer review as post-MVP. Handled in docs, but needs consistent explanation. | **Low** |
| **Debate Message DB Table** | `V1__init_schema.sql` L148 | **`SUPPORTED`** | Proposal Section 4 explicitly specifies 1–2 rounds of counter-questioning; table supports message history. | **None** |

---

## 11. Scope Drift & Unsupported Assumptions

1. **Hardcoded Spring Boot in Agent Governance Rules**:
   - *Evidence*: `.agents/rules/00-project-foundation.md` line 17: `- **Stack**: Spring Boot 3 (Java 17) + FastAPI (Python 3.12) + React 18 (Vite + TailwindCSS)`.
   - *Evidence*: Every feature rule file (`feature-course.md`, `feature-simulator.md`, etc.) specifies "Spring Boot `backend/`".
   - *Impact*: Future AI agents following `.agents/rules/` will assume Spring Boot is an unchangeable requirement, conflicting with the Project Owner's directive that backend choices are **Candidate Options only**.
2. **TailwindCSS v4 PostCSS Configuration**:
   - *Evidence*: `frontend/package.json` includes `@tailwindcss/postcss: ^4.3.3` and `tailwindcss: ^4.3.3`.
   - *Impact*: TailwindCSS v4 has breaking syntax differences from TailwindCSS v3 (which is mandated by `.agents/rules/ui-design-standards.md`).

---

## 12. Contradictions Between Project Artifacts

| Source A | Source B | Subject | Nature of Contradiction |
| :--- | :--- | :--- | :--- |
| **Proposal Section 7 & 11** ("Backend: Node.js or Python FastAPI") | **`.agents/rules/00-project-foundation.md`** ("Stack: Spring Boot 3") | Backend Framework | Direct conflict: Proposal specifies Node.js or FastAPI; project rule specifies Spring Boot. |
| **`ADR-001-TECHNOLOGY-STACK.md`** (Backend is a Candidate Option) | **`.agents/rules/feature-*.md`** (All 11 feature rule files specify Spring Boot) | Backend Finality | Inconsistency: Architectural ADR treats backend as undecided; governance rules treat Spring Boot as finalized. |
| **`ui-design-standards.md`** ("TailwindCSS v3 for all styling") | **`frontend/package.json`** (`"tailwindcss": "^4.3.3"`) | Styling Tooling | Version mismatch: Rules mandate v3; installed dependency is v4. |
| **`00-project-foundation.md`** ("React 18") | **`frontend/package.json`** (`"react": "^19.2.8"`) | Frontend Tooling | Version mismatch: Rules mandate React 18; installed dependency is React 19. |

---

## 13. Java / Spring Boot Assessment

- **Current Presence**:
  - `backend/pom.xml` defines a Spring Boot 3.3.4 parent project with Java 17.
  - Entity classes (`vn.CaseTree.*`) model the domain using Jakarta Persistence (JPA) annotations (`@Entity`, `@Table`, `@Id`, `@Enumerated`).
  - `HealthController.java` provides a minimal Spring Web MVC health check endpoint.
  - `application.yml` configures PostgreSQL, Flyway, MinIO, and Redis connections.
- **Origin**: Cloned from the engineering scaffold of `ai-teacher-copilot`.
- **Proposal Relationship**: The Proposal references `https://spring.io/projects/spring-boot` in Section 14 (Table 5 References), but Section 7 (Methodology and Tools) and Section 11 (Budget and Resources) explicitly specify `Node.js (NestJS/Express) or Python FastAPI`.
- **Current Architectural Role**: It functions as the scaffolded Backend Gateway skeleton. It does NOT contain any business implementation.
- **Architectural Impact**: If retained, it provides strong enterprise security (Spring Security), mature DB migrations (Flyway), and robust relational ORM. If migrated to Node.js (NestJS) or FastAPI, it would more closely match the body of the Proposal.
- **Owner Action Required**: The Project Owner must formally confirm whether to approve Spring Boot 3 as the Backend Gateway or order a migration to NestJS or FastAPI.

---

## 14. Business Implementation Check

Verified across the entire codebase:

| Component | Code Inspected | Result |
| :--- | :--- | :---: |
| **Authentication** | `backend/src/main/java/vn/CaseTree/auth/` | **NOT IMPLEMENTED** (no login/register controllers or JWT filters) |
| **Courses & Materials**| `backend/.../course/`, `backend/.../material/` | **NOT IMPLEMENTED** (entities exist; no CRUD services or upload streams) |
| **Case Generation** | `ai-service/app/generation/` | **NOT IMPLEMENTED** (schemas exist; no active LLM prompt chain or route) |
| **Case Review/Publish**| `backend/.../case_/`, `frontend/.../CaseReviewPage` | **NOT IMPLEMENTED** (view shell exists; no state machine update logic) |
| **Student Simulator** | `backend/.../simulation/`, `frontend/.../SimulatorPage`| **NOT IMPLEMENTED** (entity exists; no node traversal service) |
| **Argument Capture** | `backend/.../argument/` | **NOT IMPLEMENTED** (entity exists; no validation or submission service) |
| **Debate Assistant** | `ai-service/app/debate/`, `backend/.../debate/` | **NOT IMPLEMENTED** (schema exists; no prompt generation or active route) |
| **Statistics** | `backend/.../statistics/`, `frontend/.../StatisticsPage`| **NOT IMPLEMENTED** (view shell exists; no aggregation queries) |
| **Notifications** | `backend/.../notification/` | **NOT IMPLEMENTED** (package placeholder only) |
| **Evaluation** | `backend/.../evaluation/` | **NOT IMPLEMENTED** (package placeholder only) |

**Conclusion**: The repository is **100% free of business feature implementation**. It remains a pure structural skeleton.

---

## 15. Open Questions Requiring Project Owner Confirmation

1. **DEC-01 (Backend Gateway Decision)**:
   - *Question*: Will the Project Owner formally confirm **Spring Boot 3 (Java 17)** as the permanent Backend Gateway, or should a migration to **Node.js (NestJS)** or **Python FastAPI** be scheduled?
2. **DEC-02 (Notification Delivery Channel)**:
   - *Question*: Which delivery channel should be prioritized for student deadline reminders in MVP: **In-App only**, **Email only**, or **Hybrid**?
3. **DEC-03 (Classroom Trial Evaluation Method)**:
   - *Question*: For the Capstone research trial comparing AI vs. human cases, should evaluation rubrics be scored **in-platform via UI forms** or exported as **structured CSV/JSON data** for external statistical analysis?
4. **DEC-04 (Frontend Dependency Alignment)**:
   - *Question*: Should `frontend/package.json` be pinned to React 18 and TailwindCSS v3 to match `.agents/rules/ui-design-standards.md`, or should the rules be updated to permit React 19 and TailwindCSS v4?

---

## 16. Recommended Corrections (READ-ONLY — For Future Execution)

| # | Severity | Problem Area | Evidence | Recommended Correction (When Approved) | Owner Approval Needed? |
| :-: | :---: | :--- | :--- | :--- | :---: |
| **1** | **HIGH** | Hardcoded Spring Boot in `.agents/rules/` | `.agents/rules/*.md` mandate Spring Boot across 14 files | Update `.agents/rules/*.md` to use neutral "Backend Gateway" terminology, reflecting ADR-001 candidate options. | **Yes** |
| **2** | **MEDIUM**| TailwindCSS version mismatch | `package.json` has v4.3.3; rules specify v3 | Align `package.json` to TailwindCSS v3.4.x OR update `ui-design-standards.md` to approve v4. | **Yes** |
| **3** | **LOW** | React version mismatch | `package.json` has v19.2.8; rules specify v18 | Align `package.json` to React 18.3.x OR update project foundation rule to approve React 19. | **Yes** |
| **4** | **LOW** | Colloquial "workspace" comment | `LecturerLayout.tsx` line 3 uses "workspace" | Change comment to "Lecturer layout — navigation sidebar + content area". | **No** |

---

## 17. Final Verdict

### **YELLOW**
**The project direction is generally well-aligned with the Edu-Branch-AI Proposal, but contains technical inheritance debt and rule contradictions that must be formally resolved before feature development begins.**

- **Why Not GREEN?** The hardcoding of Spring Boot 3 across all `.agents/rules/` contradicts both the Proposal's primary backend options (Node.js/FastAPI) and the Project Owner's explicit directive to treat backend frameworks as candidate options. Additionally, minor frontend dependency version mismatches exist.
- **Why Not RED?** The repository has **zero scope drift** into K-12 features, strictly **zero business implementation**, flawless service boundary isolation, valid Flyway DDL syntax, and 100% valid documentation link integrity. The core pedagogical value stream (Material → RAG → Case Tree → Review → Simulator → Debate → Stats) is perfectly captured.
