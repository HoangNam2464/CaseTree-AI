# EduBranch AI — Technology & Documentation Correction Report

> **Report Type**: Post-Audit Repository Migration & Consistency Report  
> **Target System**: EduBranch AI (`https://github.com/HoangNam2464/EduBranch-AI`)  
> **Primary Authority (Priority 1)**: `C1SE_65-EduBranch-AI-Proposal_V1.0.docx`  
> **Project Owner Decisions (Priority 2)**: Ratified Backend Gateway (Node.js/NestJS), React 19 + TailwindCSS v4 baseline, 3-tier boundary, PostgreSQL+pgvector, Redis 7, MinIO, separate internal AI Service, structural skeleton only.  
> **Date of Execution**: 2026-09-11  
> **Final Consistency Verdict**: **GREEN** (All contradictions resolved, single coherent technology baseline established across Proposal, Architecture, Technology, Rules, Source Structure, and Documentation).

---

## 1. Original Problem

During the initial bootstrap scaffolding phase, structural code and architectural documentation were created by referencing the engineering patterns of `ai-teacher-copilot`. This resulted in three major architectural contradictions:
1. **Backend Framework Divergence**: The repository inherited a Java 17 / Spring Boot 3 Maven scaffold. However, the authoritative **Proposal (Sections 7 & 11)** explicitly defines the backend as **`Node.js (NestJS/Express) or Python FastAPI`**. Spring Boot only appeared as an external reference link in Table 5 and was never an approved backend technology.
2. **Rule Contradictions**: All 14 rule files in `.agents/rules/*.md` hardcoded Spring Boot 3 as a mandatory constraint, creating a direct conflict with `ADR-001-TECHNOLOGY-STACK.md` (which marked backend as an open candidate option) and with the Proposal itself.
3. **Frontend Version Drift**: `frontend/package.json` installed React 19 (`^19.2.8`) and TailwindCSS v4 (`^4.3.3`), while rules and documentation still prescribed React 18 and TailwindCSS v3.
4. **Encoding Glitch**: A UTF-8 BOM (`\ufeff`) in `ai-service/pytest.ini` broke test execution.

---

## 2. Technology Inherited from `ai-teacher-copilot`

The following technology and structural assets originated from the reference repository:

| Inherited Item | Location | Classification | Disposition | Rationale |
| :--- | :--- | :---: | :---: | :--- |
| **Spring Boot 3 / Java 17 Scaffold** | `backend/pom.xml`, `mvnw`, `src/main/java/` | `REFERENCE-DERIVED` | **REMOVED** | Conflicts with Proposal Sections 7 & 11. Replaced with Proposal-approved NestJS. |
| **JPA / Hibernate Entity Annotations** | `backend/.../entity/*.java` | `REFERENCE-DERIVED` | **REMOVED** | Replaced with TypeScript entity types in NestJS modules. |
| **Spring Security / JJWT Config** | `backend/.../config/SecurityConfig.java` | `REFERENCE-DERIVED` | **REMOVED** | Replaced with NestJS Guards / Strategies. |
| **Maven Wrapper & Profiles** | `backend/.mvn/`, `mvnw`, `pom.xml` | `REFERENCE-DERIVED` | **REMOVED** | Replaced with npm / `package.json`. |
| **"Workspace" Layout Comment** | `frontend/src/layouts/LecturerLayout.tsx` | `REFERENCE-DERIVED` | **ADAPTED** | Colloquial comment updated to standard navigation layout. |
| **`<sources>` Untrusted Prompt Boundary** | `ai-service/app/ingestion/` | `REFERENCE-DERIVED` | **KEPT** | Essential AI prompt injection defense pattern. |
| **Provider Abstraction Factory** | `ai-service/app/providers/factory.py` | `REFERENCE-DERIVED` | **KEPT** | Decouples route handlers from vendor LLM SDKs. |
| **PostgreSQL + pgvector Init Pattern** | `infrastructure/postgres/init/` | `REFERENCE-DERIVED` | **KEPT** | Robust DDL initialization for pgvector. |

---

## 3. What the EduBranch AI Proposal Actually Allows

Extracted directly from `C1SE_65-EduBranch-AI-Proposal_V1.0.docx`:

- **Backend** (Section 7, p. 11 & Section 11, p. 16):
  > *"Backend: Node.js (NestJS/Express) or Python FastAPI"*  
  `[SUPPORTED BY PROPOSAL]`
- **Frontend** (Section 7 & Section 11):
  > *"React/Next.js for the front-end, and TailwindCSS"*  
  `[SUPPORTED BY PROPOSAL]`
- **Decision Tree Canvas** (Section 11, p. 16):
  > *"Visual/graph library: ReactFlow or jsPlumb (for case-tree display)"*  
  `[SUPPORTED BY PROPOSAL]`
- **Database & Cache** (Section 11, p. 16):
  > *"Database & cache: PostgreSQL (or MongoDB), Redis"*  
  `[SUPPORTED BY PROPOSAL]`
- **AI Models & Orchestration** (Section 6 & Section 11):
  > *"AI/LLM: OpenAI GPT-4o-mini / Gemini Flash API + LangChain (for RAG orchestration and structured output)"*  
  `[SUPPORTED BY PROPOSAL]`
- **Service Boundary** (Project Owner Decision):
  > *`Frontend (Browser) → Backend Gateway → Internal AI Service (FastAPI) → LLMs`*  
  `[PROJECT OWNER DECISION]`

---

## 4. Final Selected Technology Baseline

The repository now adheres to a single, unified technology baseline:

```
┌────────────────────────────────────────────────────────┐
│  Client Tier (Browser)                                 │
│  React 19 + Vite + TypeScript + TailwindCSS v4 + Flow  │
└───────────────────────────┬────────────────────────────┘
                            │ HTTPS / REST API + JWT
                            ▼
┌────────────────────────────────────────────────────────┐
│  Backend Gateway (Node.js NestJS 10 + TypeScript)      │
│  • Auth, Users, Roles (LECTURER, STUDENT)              │
│  • Course Context & Material Metadata                  │
│  • Case Lifecycle & State Machine                      │
│  • Simulation Sessions & Student Arguments             │
│  • Debate History Persistence & 2-Round Cap            │
│  • Lecturer Statistics & Evaluation Extension          │
└────────────┬──────────────┬──────────────────┬─────────┘
             │              │                  │ Internal HTTP
             │ SQL / Schema │ S3 API           │ + X-Internal-API-Key
             ▼              ▼                  ▼
┌──────────────────┐ ┌─────────────┐ ┌───────────────────────────┐
│ PostgreSQL 16    │ │ MinIO S3    │ │ FastAPI AI Service        │
│ + pgvector       │ │ (PDF/DOCX)  │ │ (Python 3.12 — INTERNAL)  │
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

| Layer | Ratified Technology | Classification | Role |
| :--- | :--- | :---: | :--- |
| **Frontend** | React 19 + Vite + TypeScript + TailwindCSS v4 + ReactFlow | `SUPPORTED BY PROPOSAL` | Single-page application for Lecturer authoring and Student simulation. |
| **Backend Gateway** | Node.js (NestJS 10 + TypeScript) | `SUPPORTED BY PROPOSAL` | Public API Gateway, JWT security, business state machine, persistence. |
| **AI Service** | Python 3.12 + FastAPI + Pydantic v2 | `PROJECT OWNER DECISION` | Internal microservice for RAG chunking, embeddings, pgvector search, LLM prompts. |
| **Database** | PostgreSQL 16 + pgvector | `SUPPORTED BY PROPOSAL` | Unified relational and vector similarity storage. |
| **Cache & Sessions**| Redis 7 | `SUPPORTED BY PROPOSAL` | Token blacklist, session cache, rate limiting. |
| **Object Storage** | MinIO (S3-compatible) | `PROJECT OWNER DECISION` | Document storage for uploaded teaching materials (PDF/DOCX). |
| **LLMs** | Gemini 2.0 Flash / OpenAI GPT-4o-mini | `SUPPORTED BY PROPOSAL` | Fast, cost-controlled generative models. |
| **RAG Tooling** | LangChain (text-splitters) | `SUPPORTED BY PROPOSAL` | Allowed orchestration utility. |

---

## 5. Files Changed

1. `frontend/package.json` — Removed conflicting `@types/react-router-dom: ^5.3.3`.
2. `frontend/src/layouts/LecturerLayout.tsx` — Fixed comment to remove inherited "workspace" terminology.
3. `frontend/src/types/index.ts` — Updated comment from "Spring Boot" to "Backend Gateway".
4. `frontend/README.md` — Updated stack to React 19 + TailwindCSS v4 + Backend Gateway.
5. `ai-service/pytest.ini` — Re-encoded without UTF-8 BOM (`\ufeff`).
6. `docker-compose.yml` — Updated comment line 9 to reflect NestJS Gateway and React Frontend.
7. `.env.example` — Updated backend port comment, model to `gpt-4o-mini`, and internal URL comments.
8. `README.md` — Updated Tech Stack table, candidate options resolution, and directory tree.
9. `docs/PROJECT_OVERVIEW.md` — Updated architecture summary table.
10. `docs/architecture/ADR-001-TECHNOLOGY-STACK.md` — Formally ratified NestJS Backend Gateway and React 19 / TailwindCSS v4; documented deprecation of Spring Boot.
11. `docs/architecture/SERVICE-BOUNDARIES.md` — Updated diagrams and service layer descriptions.
12. `docs/architecture/SYSTEM-ARCHITECTURE.md` — Updated diagrams and technology mapping.
13. `docs/architecture/REFERENCE-REPOSITORY-AUDIT.md` — Updated backend classification to `NOT APPLICABLE / REPLACED`.
14. `docs/qa/TESTING-STRATEGY.md` — Updated backend testing to Jest / Supertest / `@nestjs/testing`.
15. `docs/ai/RAG-PIPELINE.md` — Replaced "Spring Boot" with "Backend Gateway".
16. `docs/ai/DEBATE-ASSISTANT.md` — Replaced "Spring Boot" with "Backend Gateway".
17. `.github/workflows/backend-ci.yml` — Migrated from Java 17/Maven to Node.js 20/npm.
18. `.github/workflows/ci.yml` — Migrated backend job from Maven to Node.js 20/npm.
19. 6 feature specification files (`docs/features/FEATURE-*.md`) — Cleaned status section references from `.java` to NestJS modules.

---

## 6. Files Removed

All Java / Spring Boot / Maven files from the initial bootstrap scaffold:
- `backend/pom.xml`
- `backend/mvnw`
- `backend/mvnw.cmd`
- `backend/.mvn/` (entire directory)
- `backend/src/main/java/` (entire Java source tree)
- `backend/src/test/java/` (entire Java test tree)
- `backend/src/main/resources/application.yml`
- `backend/target/` (build output)

---

## 7. Files Migrated / Created

1. `backend/migrations/V1__init_schema.sql` — Preserved standard PostgreSQL DDL schema.
2. `infrastructure/postgres/migrations/V1__init_schema.sql` — Copy preserved for infrastructure initialization.
3. `backend/package.json` — NestJS 10, TypeScript 5, dependencies installed.
4. `backend/tsconfig.json` — Standard TypeScript configuration.
5. `backend/nest-cli.json` — Nest CLI configuration.
6. `backend/src/main.ts` — NestJS bootstrap (Port 8080, `/api/v1`, CORS).
7. `backend/src/app.module.ts` — Root module wiring 11 domain modules and health check.
8. `backend/src/common/health/health.controller.ts` & `health.module.ts` — Health check endpoint (`/api/v1/health`).
9. 11 Domain Module Skeletons (pure structural placeholders, zero business logic):
   - `backend/src/modules/auth/`
   - `backend/src/modules/user/`
   - `backend/src/modules/course/`
   - `backend/src/modules/material/`
   - `backend/src/modules/case/`
   - `backend/src/modules/simulation/`
   - `backend/src/modules/argument/`
   - `backend/src/modules/debate/`
   - `backend/src/modules/statistics/`
   - `backend/src/modules/notification/`
   - `backend/src/modules/evaluation/`
10. `backend/README.md` — Updated NestJS documentation.
11. `backend/.env.example` — Node.js environment configuration template.

---

## 8. Rules Updated

All 14 files under [`.agents/rules/`](file:///d:/CAPSTONE_2026/EduBranch-AI/.agents/rules) were systematically updated:

| Rule File | Nature of Correction |
| :--- | :--- |
| `00-project-foundation.md` | Replaced Spring Boot 3 (Java 17) with Node.js (NestJS 10 + TypeScript). Replaced React 18 with React 19 + TailwindCSS v4. Replaced Java coding standards with TypeScript/NestJS standards. Updated service boundary tables. |
| `ui-design-standards.md` | Updated tech stack to React 19 + TailwindCSS v4. |
| `feature-authentication.md` | Updated scope and service owner to Backend Gateway (NestJS `backend/`). |
| `feature-course.md` | Updated scope and service owner to Backend Gateway (NestJS `backend/`). |
| `feature-material.md` | Updated scope and service owner to Backend Gateway (NestJS `backend/`). |
| `feature-case-generation.md` | Updated scope and service owner to Backend Gateway (NestJS `backend/`). |
| `feature-case-review.md` | Updated scope and service owner to Backend Gateway (NestJS `backend/`). |
| `feature-simulator.md` | Updated scope and service owner to Backend Gateway (NestJS `backend/`). |
| `feature-argument.md` | Updated scope and service owner to Backend Gateway (NestJS `backend/`). |
| `feature-debate-assistant.md`| Updated scope and service owner to Backend Gateway (NestJS `backend/`). |
| `feature-statistics.md` | Updated scope and service owner to Backend Gateway (NestJS `backend/`). |
| `feature-notification.md` | Updated scope and service owner to Backend Gateway (NestJS `backend/`). |
| `feature-evaluation.md` | Updated scope and service owner to Backend Gateway (NestJS `backend/`). |
| `feature-rag.md` | Maintained (already references Python AI Service). |

---

## 9. Validation Performed

1. **Frontend Compilation**:
   - Executed `npm run build` in `frontend/`.
   - Result: **0 errors, 41 modules transformed, clean bundle generated in 3.12s**.
2. **Backend Compilation**:
   - Executed `npm run build` in `backend/`.
   - Result: **0 errors, NestJS application compiled successfully via `nest build`**.
3. **AI Service Test Suite**:
   - Executed `python -m pytest tests/` in `ai-service/`.
   - Result: **1 passed, 0 failed in 3.52s (`tests/test_health.py::test_health PASSED [100%]`)**.
4. **Global Reference Audit**:
   - Grep search for `Spring Boot` across `.agents/rules/` → **0 matches**.
   - Grep search for `Java` across `.agents/rules/` and `docs/features/` → **0 matches**.
   - Grep search for `React 18` across `.agents/rules/` → **0 matches**.
   - Grep search for `TailwindCSS v3` across `.agents/rules/` → **0 matches**.
5. **Business Logic Verification**:
   - Verified that all 11 backend modules are pure structural skeletons.
   - Verified that AI service endpoints remain non-active placeholders.
   - **Zero business logic was implemented during this task**.

---

## 10. Remaining Project Owner Decisions

The following product-level choices from the Proposal remain open for future sprint planning:

1. **DEC-02 (Notification Delivery Channel)**:
   - *Options*: In-App notifications only vs. Email only vs. Hybrid (In-App primary, Email optional).
   - *Status*: Documented in `FEATURE-NOTIFICATIONS.md`; implementation unstarted.
2. **DEC-03 (Classroom Trial Evaluation Method)**:
   - *Options*: In-Platform manual rubric scoring by lecturers via UI vs. Structured data export (CSV/JSON) for external statistical software (SPSS/R/Excel).
   - *Status*: Documented as "Open / To Be Decided" in `FEATURE-EVALUATION-AND-RESEARCH.md`.

---

## 11. Final Consistency Verdict

### **GREEN**

The EduBranch AI repository now presents a **100% unified, consistent, and Proposal-compliant technical direction**:
- **Proposal** defines Node.js (NestJS/Express) backend and React/Tailwind frontend.
- **Architecture** ADR-001 ratifies NestJS and React 19 + TailwindCSS v4.
- **Rules** in `.agents/rules/` enforce NestJS, FastAPI, and React 19.
- **Source Code** in `backend/`, `ai-service/`, and `frontend/` cleanly compiles under these stacks.
- **Documentation** across `docs/` describes this exact system without contradictory claims.
- **Business Scope** remains 100% focused on university branching case studies and AI debate, with strictly zero K-12 leaks and zero premature feature implementation.
