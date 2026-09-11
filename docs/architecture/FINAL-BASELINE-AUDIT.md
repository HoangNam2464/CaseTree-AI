# FINAL BASELINE AUDIT — EduBranch AI
# Post-Technology-Migration Verification Report

> **Audit Date**: 2026-09-11
> **Auditor**: AI Repository Auditor (Antigravity)
> **Audit Type**: READ-ONLY — No source changes made during this audit.
> **Scope**: Full repository: source code, configuration, documentation, rules, CI/CD, Docker, environment files.
> **Approved Baseline Reference**: Confirmed Project Owner Technology Baseline (Final).

---

## 1. Executive Summary

This audit independently verifies the entire EduBranch AI repository against the confirmed Final Technology Baseline, following the technology migration from Java 17 / Spring Boot 3 to Node.js / NestJS 10.

**Overall Outcome: YELLOW**

The repository is largely correctly migrated and structurally sound. However, concrete stale-reference findings prevent a full GREEN verdict:

| # | Layer | Finding | Severity |
|---|---|---|---|
| F-01 | `ai-service/app/main.py` | Three "Spring Boot" references in comments/CORS | HIGH |
| F-02 | `ai-service/app/core/security.py` | One "Spring Boot -> FastAPI" reference in docstring | MEDIUM |
| F-03 | `ai-service/app/generation/schemas/decision_tree.py` | Two "Spring Boot" docstring references | MEDIUM |
| F-04 | `README.md` | Architecture section describes Spring Boot / Java 17 / React 18 | HIGH |
| F-05 | `CONTRIBUTING.md` | Sections B and 5 reference Java 17, Spring Boot 3, React 18 | HIGH |
| F-06 | `SECURITY.md` | Sections 1, 2, 4, 10 reference Spring Boot and JPA | MEDIUM |
| F-07 | `CHANGELOG.md` | Entry documents "Spring Boot 3 backend" as scaffolded | LOW |
| F-08 | `backend/target/` | Empty Maven target/ directory tree remains | LOW |

---

## 2. Technology Baseline Verification

### 2.1 Backend Gateway — YELLOW

| Check | Expected | Actual | Status |
|---|---|---|---|
| Runtime | Node.js 20 LTS | `@types/node: ^20.11.0`; CI: `setup-node: "20"` | PASS |
| Framework | NestJS 10 | `@nestjs/common: ^10.3.0`, `@nestjs/core: ^10.3.0` | PASS |
| Language | TypeScript 5.x | `typescript: ^5.3.3` | PASS |
| Entry point | NestJS bootstrap | `src/main.ts`: `NestFactory.create(AppModule)` | PASS |
| Spring Boot present? | None | No `pom.xml`, no `mvnw`, no `src/main/java/` | PASS |
| Maven present? | None | No `pom.xml`, no `.mvn/` | PASS |
| JPA / Hibernate? | None | Not in `package.json`, not in `src/` | PASS |
| `backend/target/` | Should not exist | Directory exists with 4 Maven subdirectories (empty, no .class files) | REMNANT |
| Spring Boot in `.ts` source | None | 0 matches in `*.ts` files | PASS |
| Spring Boot in README | None | README Mermaid diagram and text contain `Spring Boot 3` | STALE REF |
| Spring Boot in CONTRIBUTING | None | CONTRIBUTING Section B: "Backend — Java 17 + Spring Boot 3" | STALE REF |

`backend/target/` is a Maven build output directory from the removed Spring Boot scaffold. No `.class` or `.jar` files exist — it is empty directory structure only.

### 2.2 Frontend — GREEN

| Check | Expected | Actual | Status |
|---|---|---|---|
| React version | 19 | `react: ^19.2.8`, `react-dom: ^19.2.8` | PASS |
| Build tool | Vite | `vite: ^8.3.0`, `vite.config.ts` present | PASS |
| TypeScript | 5.x | `typescript: ~6.0.2` (TS6 is forward-compatible with TS5) | PASS |
| TailwindCSS | v4 | `tailwindcss: ^4.3.3`, `@tailwindcss/postcss: ^4.3.3` | PASS |
| TailwindCSS import style | v4 | `index.css`: `@import "tailwindcss"` (v4 syntax) | PASS |
| ReactFlow | 11.x | `reactflow: ^11.11.4` | PASS |
| Zustand | Present | `zustand: ^5.0.15` | PASS |
| Axios | Present | `axios: ^1.20.0` | PASS |
| Next.js dependency | None | Not in `package.json` | PASS |
| jsPlumb dependency | None | Not in `package.json` or `src/` | PASS |
| React 18 in README | None | README badge shows `React-18` (stale badge) | STALE REF |
| API client structure | `src/services/apiClient.ts` | File exists, BASE_URL points to Backend Gateway only — no FastAPI URL | PASS |

> **TypeScript 6 note**: Confirmed baseline specifies 5.x. Installed version is `~6.0.2`. TypeScript 6 is backward-compatible. Risk: LOW. Recommend noting as accepted engineering drift in ADR-001.

### 2.3 AI Service — YELLOW

| Check | Expected | Actual | Status |
|---|---|---|---|
| Runtime | Python 3.12 | Pinned in `requirements.txt`; CI: `python-version: "3.12"` | PASS |
| Framework | FastAPI | `fastapi==0.115.0` | PASS |
| Pydantic | v2 | `pydantic==2.9.2` | PASS |
| LangChain | Present | `langchain==0.3.1`, `langchain-openai`, `langchain-google-genai`, `langchain-text-splitters==0.3.0` | PASS |
| OpenAI provider | Present | `openai==1.51.0`, `providers/openai_provider.py` | PASS |
| Gemini provider | Present | `google-generativeai==0.8.3`, `providers/gemini_provider.py` | PASS |
| Provider abstraction | `providers/factory.py` | Present; `lru_cache` singleton; switches on `AI_PROVIDER` env variable | PASS |
| pgvector client | Present | `pgvector==0.3.5`, `asyncpg==0.29.0`, `psycopg2-binary==2.9.9` | PASS |
| Document parsers | Present | `pypdf==5.0.1`, `python-docx==1.1.2` | PASS |
| Spring Boot in Python source | None | Found in `main.py` (lines 5, 49, 53), `security.py` (line 4), `decision_tree.py` (lines 6, 70) | STALE REF |
| Feature routers registered | Scaffold only | All routers commented out — `# app.include_router(...)` | SKELETON CORRECT |

---

## 3. Architecture Verification

### 3.1 Service Boundary Enforcement — GREEN

| Rule | Evidence | Status |
|---|---|---|
| Frontend calls Backend Gateway only | `apiClient.ts`: BASE_URL points to `http://localhost:8080/api` — no FastAPI URL anywhere in `frontend/src/` | ENFORCED |
| Backend Gateway is the API gateway | `main.ts`: global prefix `/api/v1`, CORS restricted to frontend origin | ENFORCED |
| AI Service is internal only | `main.py`: `docs_url=None` in production; CORS restricted to port 8080; `verify_internal_api_key` dependency | ENFORCED |
| AI Service must not be internet-exposed | Docker Compose: AI Service not defined as a public service; `main.py` docstring: "INTERNAL ONLY" | ENFORCED |
| Internal authentication | `security.py`: `X-Internal-API-Key` header validation via FastAPI dependency injection | ENFORCED |

### 3.2 Architecture Diagram Accuracy — RED (Documentation layer only)

Source code correctly implements `Frontend -> Backend Gateway -> Internal AI Service`.

However, `README.md`, `CONTRIBUTING.md`, and `SECURITY.md` portray the old `Frontend -> Spring Boot -> FastAPI` boundary in text, diagrams, and examples. This is a documentation problem only and does not affect runtime behavior.

---

## 4. Infrastructure Verification — GREEN

| Service | Expected | Docker Image | Status |
|---|---|---|---|
| PostgreSQL | 16 + pgvector | `pgvector/pgvector:pg16` | CORRECT |
| Redis | 7 | `redis:7-alpine` | CORRECT |
| MinIO | S3-compatible | `minio/minio:latest` | CORRECT |
| pgvector extension | Enabled | Baked into `pgvector/pgvector:pg16` image | CORRECT |
| Health checks | All services | Defined for postgres, redis, minio | CORRECT |
| Network isolation | Single internal network | `edubranch_network` bridge network | CORRECT |

`.env.example` correctly documents `SERVER_PORT=8080` (NestJS), `FASTAPI_PORT=8000` (AI Service), `DEBATE_MAX_ROUNDS=2`, and all infrastructure connection variables. No Spring Boot-specific variables are present.

---

## 5. AI / RAG Verification — GREEN (Documentation and Skeleton)

| Requirement | Verification Source | Status |
|---|---|---|
| RAG pipeline: Material -> Extract -> Chunk -> Embed -> pgvector -> Retrieve -> Generate | `docs/ai/RAG-PIPELINE.md` + `ai-service/app/` package structure | DOCUMENTED |
| Structured output / JSON Schema for case generation | `ai-service/app/generation/schemas/decision_tree.py` | SCHEMA PRESENT |
| Decision tree BFS cycle detection | `decision_tree.py` schema references `validate_tree_structure` | DOCUMENTED |
| Lecturer review/approval required before publication | `DRAFT -> REVIEWED -> APPROVED -> PUBLISHED` in `00-project-foundation.md` section 4 | RULE ENFORCED |
| Debate max 2 rounds | `DEBATE_MAX_ROUNDS=2` in `.env.example`; rule in `00-project-foundation.md` section 6 | RULE + CONFIG ENFORCED |
| Debate does not grade | `copilot-instructions.md` section 4; `00-project-foundation.md` section 6; `SECURITY.md` section 6 | RULE ENFORCED |
| Debate does not decide pass/fail | Same governance files | RULE ENFORCED |
| Sources boundary | `00-project-foundation.md` section 6 Rule 1; `copilot-instructions.md` section 4 | RULE ENFORCED |
| Provider abstraction | `providers/factory.py` + `base.py` + `gemini_provider.py` + `openai_provider.py` | IMPLEMENTED (skeleton) |

All entries above are structural skeleton and documentation only. No functional business implementation exists, which is the correct expected state.

---

## 6. Product Scope Verification — GREEN

### Features Present — In Scope (Correct)

- Authentication and Roles (`auth/`, `user/` modules)
- Course and Material Metadata (`course/`, `material/` modules)
- Document Processing / RAG (`ingestion/`, `retrieval/` packages)
- AI Case Generation (`generation/` package, decision tree schema)
- Lecturer Review / Edit / Approval (case lifecycle documented)
- Case Publishing (`case/` module, DRAFT->PUBLISHED lifecycle)
- Student Simulator (`simulation/` module)
- Student Arguments (`argument/` module)
- AI Debate Assistant (`debate/` module and package)
- Lecturer Statistics (`statistics/` module)
- Notifications (`notification/` module — extension point)
- Evaluation / Research boundary (`evaluation/` module and package)

### Out-of-Scope Features — All ABSENT

| Feature | Result |
|---|---|
| Lesson planning | Not found in source or rules |
| Quiz generation | Not found in source or rules |
| Exam generation | Not found in source or rules |
| Bloom's taxonomy | Found only in historical audit docs explicitly marking it as EXCLUDED |
| K-12 functionality | Not found in active source or rules |
| Autonomous grading | Not found in source; explicitly forbidden in rules |
| LMS integration | Not found |
| Social login | Not found |

---

## 7. Structural Skeleton Verification — GREEN

### Backend (`backend/src/modules/`)

- 11 domain directories: `auth/`, `user/`, `course/`, `material/`, `case/`, `simulation/`, `argument/`, `debate/`, `statistics/`, `notification/`, `evaluation/`
- Each module contains only a `*.module.ts` file (module registration only — no business logic)
- No controllers, services, repositories, or DTOs implemented

### AI Service (`ai-service/app/`)

- 7 packages: `core/`, `providers/`, `ingestion/`, `retrieval/`, `generation/`, `debate/`, `evaluation/`
- `main.py`: all feature routers are commented out
- Implemented code only: health endpoint, global exception handler, `core/` utilities, `providers/` factory and LLM clients, `generation/schemas/` Pydantic schemas

### Frontend (`frontend/src/`)

- Feature directories exist: `features/`, `components/`, `layouts/`, `pages/`, `services/`, `stores/`, `types/`, `hooks/`, `utils/`
- Implemented code only: `apiClient.ts`, `authStore.ts`, layout shells, routing shell, CSS baseline

### Confirmed Not Implemented

| Feature | Status |
|---|---|
| Authentication workflow (JWT, login, registration) | Not implemented |
| RAG retrieval pipeline | Not implemented |
| LLM case generation | Not implemented |
| Simulator workflow | Not implemented |
| Debate workflow | Not implemented |
| Statistics aggregation | Not implemented |
| Notification workflow | Not implemented |
| Research/evaluation data export | Not implemented |

---

## 8. Documentation Verification — YELLOW

### Correctly Updated Documents

| File | Status |
|---|---|
| `docs/architecture/ADR-001-TECHNOLOGY-STACK.md` | CORRECT — NestJS 10, React 19, ratified decisions |
| `docs/architecture/SYSTEM-ARCHITECTURE.md` | CORRECT — NestJS baseline |
| `docs/architecture/SERVICE-BOUNDARIES.md` | CORRECT — boundary documentation |
| `docs/architecture/TECHNOLOGY-CORRECTION-REPORT.md` | CORRECT — migration history |
| `docs/features/FEATURE-*.md` (11 files) | CORRECT — technology-neutral or NestJS-correct |
| `.env.example` | CORRECT — no Spring Boot references |
| `docker-compose.yml` | CORRECT — no Spring Boot |
| `.github/workflows/backend-ci.yml` | CORRECT — Node.js 20 / NestJS build |
| `.github/workflows/ci.yml` | CORRECT — Node.js 20 / Python 3.12 / React |
| `.github/copilot-instructions.md` | CORRECT — describes NestJS boundary |

### Documents with Stale Content — Require Update

| File | Stale Content | Severity |
|---|---|---|
| `README.md` | Mermaid diagram shows Spring Boot 3 / Java 17; text: "Frontend -> Spring Boot only"; Testing: `./mvnw test`; Prerequisites: Java JDK 17+; badges: Java-17, React-18 | HIGH |
| `CONTRIBUTING.md` | Section 3A heading: "React 18"; Section 3B heading: "Backend — Java 17 + Spring Boot 3"; Section 5 table: "Frontend -> Spring Boot only"; Section 6: "at the Spring Boot layer" | HIGH |
| `SECURITY.md` | Section 1: "Spring Boot handles all authentication"; Section 2: "Spring Boot enforces ownership"; Section 4: "Spring Boot and FastAPI"; Section 10: "JPA/Spring Data repositories" | MEDIUM |
| `CHANGELOG.md` | Entry: "Spring Boot 3 backend project structure" — incomplete historical record | LOW |
| `ai-service/app/main.py` | Line 5: "called exclusively by the Spring Boot backend"; Line 49: "CORS: Accept only from Spring Boot"; Line 53 comment: "Spring Boot only" | HIGH |
| `ai-service/app/core/security.py` | Line 4: "Spring Boot -> FastAPI communication" | MEDIUM |
| `ai-service/app/generation/schemas/decision_tree.py` | Line 6: "before returning to Spring Boot"; Line 70: "before forwarding to Spring Boot" | MEDIUM |

---

## 9. Rule Verification — GREEN

All 14 `.agents/rules/` files were audited by direct inspection and full-repository grep.

| Rule File | Spring Boot? | Java? | React 18? | Tailwind v3? | Status |
|---|---|---|---|---|---|
| `00-project-foundation.md` | None | None | None | None | CORRECT |
| `ui-design-standards.md` | None | None | None | None | CORRECT |
| `feature-authentication.md` | None | None | n/a | n/a | CORRECT |
| `feature-case-generation.md` | None | None | n/a | n/a | CORRECT |
| `feature-case-review.md` | None | None | n/a | n/a | CORRECT |
| `feature-argument.md` | None | None | n/a | n/a | CORRECT |
| `feature-course.md` | None | None | n/a | n/a | CORRECT |
| `feature-debate-assistant.md` | None | None | n/a | n/a | CORRECT |
| `feature-evaluation.md` | None | None | n/a | n/a | CORRECT |
| `feature-material.md` | None | None | n/a | n/a | CORRECT |
| `feature-notification.md` | None | None | n/a | n/a | CORRECT |
| `feature-rag.md` | None | None | n/a | n/a | CORRECT |
| `feature-simulator.md` | None | None | n/a | n/a | CORRECT |
| `feature-statistics.md` | None | None | n/a | n/a | CORRECT |

Full-repository grep across `.agents/rules/`: 0 matches for "Spring Boot", "Java", "React 18", "TailwindCSS v3".

The active agent rule baseline is correct and consistent with the approved technology baseline.

---

## 10. Global Obsolete-Reference Scan

Full repository scan (excluding `node_modules/`, `.pytest_cache/`, `dist/`):

| Term | Locations | Classification |
|---|---|---|
| `Spring Boot` | `ai-service/app/main.py` (3x), `ai-service/app/core/security.py` (1x), `ai-service/app/generation/schemas/decision_tree.py` (2x) | OBSOLETE / STALE COMMENT |
| `Spring Boot` | `README.md` (architecture + testing + prerequisites) | CONFLICTING |
| `Spring Boot` | `CONTRIBUTING.md` (Section B heading, Section 5 table, Section 6 rule) | CONFLICTING |
| `Spring Boot` | `SECURITY.md` (Sections 1, 2, 4, 10) | CONFLICTING |
| `Spring Boot` | `CHANGELOG.md` (scaffold entry) | VALID HISTORICAL RECORD |
| `Spring Boot` | `docs/architecture/PROJECT-DIRECTION-AUDIT.md`, `TECHNOLOGY-CORRECTION-REPORT.md`, `BOOTSTRAP-AUDIT.md`, `REFERENCE-REPOSITORY-AUDIT.md` | VALID HISTORICAL RECORD |
| `Spring Boot` | `docs/architecture/ADR-001-TECHNOLOGY-STACK.md` Section 4 ("Inherited Spring Boot... removed") | VALID HISTORICAL RECORD |
| `backend/target/` | Empty Maven directory tree (4 subdirs, 0 files) | ACCIDENTAL REMNANT |
| `React 18` | `README.md` badge only | CONFLICTING |
| `Java 17` | `README.md` (badge, Prerequisites, Mermaid), `CONTRIBUTING.md` Section B | CONFLICTING |
| `JPA` | `CONTRIBUTING.md` (entity exposure rule), `SECURITY.md` Section 10 | CONFLICTING |
| `./mvnw` | `README.md` Section 3 Local Dev instructions | CONFLICTING |
| `Bloom` | Historical audit docs only — explicitly marking it as EXCLUDED | VALID HISTORICAL RECORD |
| `Next.js` | `scratch_proposal_full.txt` (Proposal text), historical audit docs | VALID HISTORICAL RECORD |
| `Next.js` | `node_modules/` (library READMEs, oxlint schema) | VALID — THIRD-PARTY DEPENDENCY INTERNALS |
| `jsPlumb` | Not found anywhere | CLEAN |
| `TailwindCSS v3` | Not found anywhere | CLEAN |
| `Hibernate` | Not found anywhere | CLEAN |
| `Maven` | Historical docs only | VALID HISTORICAL RECORD |

---

## 11. Proposal Traceability

| Technology Decision | Classification | Basis |
|---|---|---|
| React (frontend framework) | PROPOSAL-SUPPORTED | Section 7 and 11: "React.js / Next.js" |
| TailwindCSS (UI library) | PROPOSAL-SUPPORTED | Section 11: "TailwindCSS" |
| ReactFlow (decision tree) | PROPOSAL-SUPPORTED | Section 11: "ReactFlow or jsPlumb" |
| Node.js / NestJS (backend gateway) | PROPOSAL-SUPPORTED | Section 7 and 11: "Node.js (NestJS/Express)" |
| Python / FastAPI (AI service) | PROPOSAL-SUPPORTED | Section 7 and 11: "Python FastAPI" |
| LangChain (RAG orchestration) | PROPOSAL-SUPPORTED | Section 11: "LangChain (for RAG orchestration)" |
| OpenAI GPT-4o-mini | PROPOSAL-SUPPORTED | Section 6 and 11: "OpenAI GPT-4o-mini" |
| Google Gemini Flash | PROPOSAL-SUPPORTED | Section 6 and 11: "Gemini Flash API" |
| PostgreSQL (relational DB) | PROPOSAL-SUPPORTED | Section 11: "PostgreSQL" |
| Redis (cache) | PROPOSAL-SUPPORTED | Section 11: "Redis" |
| pgvector (vector store) | PROJECT-OWNER DECISION | Not in Proposal by name; Project Owner confirmed to unify vector + relational DB |
| MinIO (object storage) | PROJECT-OWNER DECISION | Not in Proposal; Project Owner selected S3-compatible local storage |
| React 19 (specific version) | PROJECT-OWNER / ENGINEERING CHOICE | Proposal says "React"; version 19 confirmed by Project Owner |
| NestJS 10 (specific version) | PROJECT-OWNER / ENGINEERING CHOICE | Proposal says "NestJS"; version 10 is current stable |
| TailwindCSS v4 (specific version) | PROJECT-OWNER / ENGINEERING CHOICE | Proposal says "TailwindCSS"; v4 selected for modern CSS engine |
| ReactFlow 11.x (specific version) | ENGINEERING CHOICE | Proposal says "ReactFlow"; 11.x is current stable |
| PostgreSQL 16 (specific version) | ENGINEERING CHOICE | Proposal says "PostgreSQL"; 16 is current LTS |
| Redis 7 (specific version) | ENGINEERING CHOICE | Proposal says "Redis"; 7 is current stable |
| Provider abstraction pattern | ENGINEERING CHOICE | Proposal implies dual-provider; abstraction is engineering implementation |
| Vite (build tool) | ENGINEERING CHOICE | Proposal does not specify; Vite is standard for React + TypeScript |
| Zustand (state management) | ENGINEERING CHOICE | Proposal does not specify; Zustand is in project rules |
| Axios (HTTP client) | ENGINEERING CHOICE | Proposal does not specify; Axios is in project rules |
| Pydantic v2 (AI service validation) | ENGINEERING CHOICE | Proposal does not specify version; v2 is current |

---

## 12. Contradictions Found

| ID | Contradiction | Locations | Impact |
|---|---|---|---|
| C-01 | README.md Mermaid diagram and text describe Spring Boot 3 / Java 17 backend. Actual backend is NestJS 10 / Node.js 20. | README.md lines 87-113, 212, 245-248, 277-278 | HIGH — Public-facing document describes wrong stack |
| C-02 | CONTRIBUTING.md Section B: "Backend — Java 17 + Spring Boot 3"; Section 3A: "React 18"; Section 5: "Frontend -> Spring Boot only" | CONTRIBUTING.md lines 63, 77-88, 126, 131, 141 | HIGH — Developer guide is wrong for backend |
| C-03 | SECURITY.md Sections 1, 2, 4, 10 attribute auth and DB access to "Spring Boot" / "JPA". Actual is NestJS with pg driver. | SECURITY.md lines 34, 43, 58, 102 | MEDIUM — Security policy describes wrong technology |
| C-04 | ai-service/app/main.py identifies the upstream caller as "Spring Boot" in three places. Actual caller is NestJS. | main.py lines 5, 49, 53 | HIGH — Code-level stale reference visible to developers |
| C-05 | ai-service/app/core/security.py docstring: "Spring Boot -> FastAPI communication" | security.py line 4 | MEDIUM — Developer-visible stale reference |
| C-06 | ai-service/app/generation/schemas/decision_tree.py docstrings: "before returning to Spring Boot" (twice) | decision_tree.py lines 6, 70 | MEDIUM — Schema docstring is incorrect |
| C-07 | backend/target/ directory exists — a Maven build output from the removed scaffold. No .class or .jar files present. | backend/target/ | LOW — Cosmetic artifact |
| C-08 | CHANGELOG.md documents "Spring Boot 3 backend" as scaffolded with no NestJS migration entry. | CHANGELOG.md line 13 | LOW — Incomplete historical record |
| C-09 | ADR-001 status header reads "Candidate Options Documented (Backend pending Project Owner confirmation)" but body documents NestJS as ratified. | ADR-001-TECHNOLOGY-STACK.md line 3 | LOW — Minor header inconsistency |

---

## 13. Remaining Risks

| Risk | Description | Severity | Recommendation |
|---|---|---|---|
| R-01 Documentation Drift | README.md, CONTRIBUTING.md, SECURITY.md present the wrong backend technology. Any new team member would believe the backend is Spring Boot 3. | HIGH | Update in next working session |
| R-02 AI Service Stale Comments | main.py, security.py, decision_tree.py contain "Spring Boot" references. Future AI agents reading these files may incorrectly infer the backend framework. | HIGH | Update in next working session |
| R-03 Maven Target Directory | backend/target/ with Maven subdirectories creates unnecessary confusion about whether a Java build ever ran. | LOW | Delete directory; verify target/ is in backend/.gitignore |
| R-04 TypeScript Version Overshoot | typescript: ~6.0.2 exceeds the confirmed 5.x baseline. TypeScript 6 is backward-compatible. | LOW | Note in ADR-001 as accepted engineering drift |
| R-05 ADR-001 Status Header | Status line still reads "Candidate Options Documented (Backend pending...)" despite NestJS being ratified. | LOW | Update status line to "Ratified — 2026-09-11" |
| R-06 CHANGELOG Incompleteness | NestJS migration is not recorded. Only the original Spring Boot scaffold entry exists. | LOW | Add a migration entry to CHANGELOG |

---

## 14. Final Verdict

### Technology Baseline: YELLOW

All active source code and dependency configuration (package.json, requirements.txt, docker-compose.yml, CI workflows, .env.example) correctly implement the approved baseline.

YELLOW because stale "Spring Boot" references remain in ai-service Python source file comments and docstrings (findings F-01 through F-03). These do not affect runtime behavior but are code-level inconsistencies.

### Architecture: GREEN

The three-tier boundary `Frontend -> Backend Gateway -> Internal AI Service` is correctly implemented in source code:
- `apiClient.ts` calls only the Backend Gateway
- `main.py` restricts CORS to Backend Gateway origin only
- Internal API key enforcement (`X-Internal-API-Key`) is present in `security.py`
- No FastAPI endpoint is callable from the frontend

### Documentation: RED

`README.md`, `CONTRIBUTING.md`, and `SECURITY.md` actively describe the wrong technology stack. These are not historical archive files; they are living developer guides. A developer reading them would believe the backend is Java 17 / Spring Boot 3.

The ai-service Python source files also contain stale docstrings that describe the wrong calling service.

### Rules: GREEN

All 14 `.agents/rules/` files are correctly updated. Zero Spring Boot, Java, React 18, or TailwindCSS v3 references found. Rules correctly govern agent behavior under the approved baseline.

### Product Scope: GREEN

No out-of-scope functionality (lesson planning, quiz generation, K-12 features, autonomous grading, LMS integration) is present in any active source file or rule. All Bloom's taxonomy references exist only in historical audit documents that explicitly mark it as excluded.

### Business Implementation: STRUCTURAL SKELETON ONLY (CONFIRMED)

No business feature logic has been implemented. All NestJS modules are registration-only skeletons. AI service feature routers are commented out. Frontend service/store/page files are empty shells.

---

> **AUDIT COMPLETE — READ-ONLY — NO CHANGES MADE**
> Produced: `docs/architecture/FINAL-BASELINE-AUDIT.md`
> Corrections applied: See ## Post-Correction Status below.

---

## Post-Correction Status

Applied: 2026-09-11 | Corrections: C-01 through C-07

### C-01 — README.md

**Status: FIXED**

Changes applied:
- Badge strip: Replaced `Java-17` badge with `Node.js-20` and `NestJS-10` badges. Replaced `React-18` badge with `React-19`.
- Mermaid architecture diagram: Replaced `React 18 + Vite` node → `React 19 + Vite`. Replaced `Backend Gateway (Java 17)` subgraph title + `Spring Boot 3` node → `Backend Gateway (Node.js 20)` subgraph + `NestJS 10` node. Updated all diagram edges: `SB` → `NJ`, `JPA / Flyway` label → `pg driver / SQL Migrations`, `API Key` label → `X-Internal-API-Key`. Updated LLM label to `Gemini 2.0 Flash / OpenAI GPT-4o-mini`.
- Architecture Principles: "Frontend → Spring Boot only" → "Frontend → Backend Gateway only". "FastAPI is internal" → "AI Service is internal".
- Prerequisites: Removed `Java JDK 17+` row. Listed `Node.js 20 LTS` at top.
- Step 3 backend startup command: `./mvnw spring-boot:run` → `npm install && npm run start:dev`. Health check URL corrected to `/api/v1/health`.
- Testing section: `cd backend && ./mvnw test` → `cd backend && npm run test`.

Validation: `npm run build` (backend) — **exit code 0**. `npm run build` (frontend) — **exit code 0, 41 modules transformed**.

### C-02 — CONTRIBUTING.md

**Status: FIXED**

Changes applied:
- `chore` commit example: `upgrade spring-boot to 3.3.x` → `upgrade nestjs to 10.x`.
- Section 3A heading: `React 18 + TypeScript + Vite` → `React 19 + TypeScript + Vite`.
- Section 3B heading: `Backend — Java 17 + Spring Boot 3` → `Backend Gateway — Node.js 20 + NestJS 10 + TypeScript`.
- Section 3B layered architecture description: Replaced Spring Boot/JPA rules with NestJS module architecture rules (DTOs with `class-validator`, NestJS Guards, NestJS Interceptors, module-by-feature structure).
- Section 5 architecture table: `Frontend → Spring Boot only` → `Frontend → Backend Gateway only`. `FastAPI is internal` corrected. `Never leak Spring Boot business logic` → `Never leak Backend Gateway business logic`.
- Section 6 security rule: `at the Spring Boot layer` → `at the Backend Gateway (NestJS) layer`.

Validation: Frontend and backend builds passed (above). CONTRIBUTING.md contains no Spring Boot, Java 17, or React 18 references in active sections.

### C-03 — ai-service/app/main.py

**Status: FIXED**

Changes applied:
- Module docstring line 5: "called exclusively by the Spring Boot backend" → "called exclusively by the NestJS Backend Gateway".
- CORS comment line 49: "CORS: Accept only from Spring Boot (internal network)" → "CORS: Accept only from the Backend Gateway (NestJS — internal network)".
- Inline CORS comment line 53: "Spring Boot only" → "Backend Gateway only".

Runtime behavior: UNCHANGED. CORS `allow_origins` value `http://localhost:8080` is unmodified.

Validation: `pytest tests/ -v` — **1 passed** (test_health).

### C-04 — SECURITY.md

**Status: FIXED**

Changes applied:
- Section 1 (Authentication): "Spring Boot handles all authentication via JWT" → "The Backend Gateway (NestJS) handles all authentication via JWT".
- Section 2 (Authorization): "Spring Boot enforces ownership" → "The Backend Gateway (NestJS) enforces ownership".
- Section 4 (Internal Service Protection): "Communication between Spring Boot and FastAPI" → "Communication between the Backend Gateway (NestJS) and the AI Service requires a shared internal API key (X-Internal-API-Key header)". "FastAPI must only listen" → "The AI Service must only listen".
- Section 10 (Database Security): "JPA/Spring Data repositories — no raw SQL string concatenation" → "Backend Gateway repository layer — no raw SQL string concatenation".

No new security mechanisms invented. All descriptions reflect mechanisms structurally present in the codebase.

### C-05 — ai-service/app/core/security.py

**Status: FIXED**

Changes applied:
- Docstring line 4: "Validates the internal API key used for Spring Boot → FastAPI communication." → "Validates the internal API key used for Backend Gateway → Internal AI Service communication."

Security implementation logic (HTTPException, `X-Internal-API-Key` header validation, `verify_internal_api_key` dependency function): UNCHANGED.

### C-06 — ai-service/app/generation/schemas/decision_tree.py

**Status: FIXED**

Changes applied:
- Module docstring line 6: "before returning to Spring Boot" → "before forwarding to the Backend Gateway (NestJS)".
- `CaseGenerationOutput` class docstring line 70: "before forwarding to Spring Boot" → "before forwarding to the Backend Gateway (NestJS)".

Decision tree Pydantic schema structure, field definitions, `validate_tree_structure` model validator, `_check_no_cycles` BFS cycle detection: ALL UNCHANGED.

### C-07 — backend/target/

**Status: FIXED**

Action: `Remove-Item -Recurse -Force "d:\CAPSTONE_2026\EduBranch-AI\backend\target"` — **exit code 0**.

The empty Maven build output directory (`target/generated-sources/`, `target/test-classes/`, etc.) has been deleted. Verified: no `.class`, `.jar`, or active source files were present in the directory.

---

## Global Post-Fix Scan Results

Full-repository scan performed across `*.py`, `*.ts`, `*.tsx`, `*.md`, `*.yml`, `*.yaml` after all corrections.

| Term | Active Files with Conflicting References | Historical/Archive References | Status |
|---|---|---|---|
| `Spring Boot` | **0** | CHANGELOG.md (scaffold entry); ADR-001 §4; TECHNOLOGY-CORRECTION-REPORT.md; BOOTSTRAP-AUDIT.md; PROJECT-DIRECTION-AUDIT.md; FINAL-BASELINE-AUDIT.md (audit record) | CLEAN |
| `Java 17` | **0** | Same historical audit docs | CLEAN |
| `React 18` | **0** in active files; `node_modules/` only (third-party lib internals) | Historical audit docs | CLEAN |
| `JPA` | **0** | None | CLEAN |
| `Hibernate` | **0** | None | CLEAN |
| `mvnw` | **0** | None | CLEAN |
| `Maven` | **0** in active files | Historical audit docs (valid) | CLEAN |
| `TailwindCSS 3` | **0** | None | CLEAN |

---

## Post-Correction Validation Results

| Check | Result |
|---|---|
| Backend build (`npm run build` in `backend/`) | PASS — exit code 0 |
| Frontend build (`npm run build` in `frontend/`) | PASS — exit code 0, 41 modules transformed |
| AI Service tests (`pytest tests/ -v` in `ai-service/`) | PASS — 1 passed, 0 failed |
| Global Spring Boot grep (active files) | PASS — 0 conflicting occurrences |
| Global Java 17 grep (active files) | PASS — 0 conflicting occurrences |
| Global React 18 grep (active files) | PASS — 0 occurrences (node_modules only) |
| Global JPA / Hibernate / mvnw grep (active files) | PASS — 0 occurrences |
| backend/target/ removed | PASS — directory deleted |
| Structural skeleton intact | PASS — no business logic added |
| Architecture boundary intact | PASS — Frontend → Gateway → AI Service unchanged |
| `.agents/rules/` unchanged | PASS — all 14 rule files unmodified |

---

## Updated Final Verdicts (Post-Correction)

### Technology Baseline: GREEN

All active source code and dependency configuration correctly implement the approved baseline. All stale "Spring Boot" references have been removed from ai-service Python source files. No conflicting technology references remain in any active file.

### Architecture: GREEN

The three-tier boundary `Frontend → Backend Gateway → Internal AI Service` is correctly implemented in source code AND correctly documented in README.md, CONTRIBUTING.md, and SECURITY.md. CORS, API key enforcement, and client-side API routing are unchanged.

### Documentation: GREEN

README.md, CONTRIBUTING.md, and SECURITY.md now correctly describe the NestJS 10 / Node.js 20 Backend Gateway. Architecture diagrams, prerequisites, startup commands, testing commands, and security policies all reflect the approved baseline. No active document describes Spring Boot or Java 17 as the backend.

### Rules: GREEN (UNCHANGED)

All 14 `.agents/rules/` files remain correct. Zero Spring Boot, Java, React 18, or TailwindCSS v3 references found. No rule files were modified in this correction session.

### Product Scope: GREEN (UNCHANGED)

No out-of-scope functionality is present in any active source file or rule.

### Business Implementation: STRUCTURAL SKELETON ONLY (CONFIRMED)

No business feature logic was added during this correction session. The repository remains a structural skeleton only.

---

> **CORRECTIONS COMPLETE**
> Findings C-01 through C-07 have been resolved.
> All validation checks passed.
> Repository documentation is now consistent with the approved EduBranch AI Technology Baseline.

