# CaseTree AI — Post-Scaffold Audit, Alignment & Self-Audit Report

> **Document Status**: Authoritative Final Post-Scaffold Self-Audit  
> **Date**: 2026-09-11  
> **Authoritative Sources**:
> 1. `C1SE_65-CaseTree-AI-Proposal_V1_1.docx` (Product Source of Truth — Updated to Proposal V1.1)
> 2. Explicit Project Owner Decisions (Service boundary, PostgreSQL+pgvector, Redis, MinIO, AI-service separation)
> 3. Repository Governance Rules (`.agents/rules/`, `.github/copilot-instructions.md`)

---

## 1. Current Repository State

The repository contains a clean, verified multi-tier skeleton following initial scaffolding by Claude Sonnet 4.6 and post-scaffold alignment:
- **`backend/`**: Contains domain entity definitions, JPA mappings, Flyway database migration scripts, security configuration shells, and health check endpoints.
- **`ai-service/`**: Contains FastAPI configuration, Pydantic v2 schemas for decision tree structures, graph cycle detection utilities, provider abstraction interfaces, and an unauthenticated `/health` endpoint.
- **`frontend/`**: Contains React 18 + Vite + TypeScript application setup, TailwindCSS configuration, ReactFlow graph integration shells, Zustand stores, Axios API client, and layout/page shells.
- **`infrastructure/`**: Contains `docker-compose.yml` orchestrating PostgreSQL 16 with `pgvector`, Redis 7, and MinIO object storage.
- **`docs/`**: Comprehensive documentation architecture including ADRs, architecture diagrams, sequence data flows, service boundaries, 11 detailed feature specifications, proposal traceability matrix, reference audit, and research design.
- **`Feature Implementation State`**: **STRICTLY ZERO BUSINESS FEATURES IMPLEMENTED**. The codebase remains a pure architectural skeleton.

---

## 2. Proposal Alignment

A comprehensive audit against `C1SE_65-CaseTree-AI-Proposal_V1.0.docx` confirms:
- **Project Identity**: Fully compliant. CaseTree AI is established as an AI platform for interactive branching case studies and open review in university teaching (for Lecturers and Students).
- **Core Value Stream**: Fully compliant. Grounded in teaching material → RAG retrieval → Structured decision tree generation → Mandatory lecturer review & approval → Student simulation → Consequence reveal & argument justification → AI Debate Assistant (Devil's Advocate 1–2 rounds max, no grading) → Lecturer statistics.
- **Target Audience**: University education (NOT K-12).
- **Scope Compliance**:
  - In-Scope features: Completely documented across 11 feature specifications and 30 traceability items.
  - Out-of-Scope features: Excluded (no lesson planners, quiz generators, teacher workspaces, LMS integrations, social logins, or autonomous grading).
- **Proposal Alignment Status**: **Fully Aligned**.

---

## 3. Owner Decisions

The following explicit Project Owner decisions have been verified and applied:
1. **Reference Repository Role**: `ai-teacher-copilot` is treated as an engineering reference only. Zero source code and zero K-12 business logic have been copied.
2. **Architecture Boundary**: Confirmed service hierarchy: `Frontend (Browser) → Backend Gateway → AI Service (Internal Only)`. Direct frontend access to the AI service is strictly forbidden.
3. **AI Service Separation**: AI service is isolated as a dedicated FastAPI microservice inside the internal Docker network.
4. **Data & Storage Infrastructure**: PostgreSQL 16 + pgvector confirmed for relational business data and vector embeddings; Redis 7 confirmed for caching and session management; MinIO confirmed for PDF/DOCX object storage.
5. **No Business Feature Implementation**: The repository remains strictly a skeleton with detailed documentation specifications in `docs/*.md`.
6. **Backend Candidate Status**: Backend framework is maintained as an open candidate option pending final owner confirmation.

---

## 4. Reference Repository Alignment

An audit of `ai-teacher-copilot` was completed in [`docs/architecture/REFERENCE-REPOSITORY-AUDIT.md`](REFERENCE-REPOSITORY-AUDIT.md):
- **Reusable Engineering Rules Adopted**: Git Feature Branch workflow (`feature/* → develop → main`), Conventional Commits (`type(scope): description`), PR checklist templates, PEP8 / Black / Flake8 standards, layered backend architecture, and untrusted data prompt boundaries (`<sources>...</sources>`).
- **Reusable Architectural Patterns Adopted**: LLM Provider Abstraction (`providers/factory.py`), internal service API token authentication (`X-Internal-API-Key`), pgvector cosine similarity retrieval queries, and Pydantic v2 structured output validation.
- **Reference Features Excluded**: Lesson Planner, Exam/Quiz Generator, Teacher Workspace, Word Export, Bloom's Taxonomy, and Autonomous Rubric Grading.

---

## 5. Architecture

The confirmed system architecture is documented in [`SYSTEM-ARCHITECTURE.md`](SYSTEM-ARCHITECTURE.md), [`SERVICE-BOUNDARIES.md`](SERVICE-BOUNDARIES.md), and [`DATA-FLOW.md`](DATA-FLOW.md):
- **Client Tier**: React 18 + Vite + TypeScript + TailwindCSS + ReactFlow.
- **Backend Gateway**: Candidate Options: Spring Boot 3 (scaffolded) / Node.js (NestJS) / Python FastAPI. Acts as the single external API gateway for the frontend.
- **AI Service**: Python 3.12 + FastAPI (internal only). Owns document parsing, chunking, embeddings, pgvector retrieval, case generation prompt engineering, and debate assistance.
- **Persistence**: PostgreSQL 16 + pgvector, Redis 7, MinIO.
- **LLMs**: Google Gemini 2.0 Flash / OpenAI GPT-4o-mini via provider abstraction.

---

## 6. Documentation

The documentation architecture is established without duplicate sources of truth:
1. **Architecture & Standards**:
   - [`ADR-001-TECHNOLOGY-STACK.md`](ADR-001-TECHNOLOGY-STACK.md): Full stack classification & candidate options.
   - [`SYSTEM-ARCHITECTURE.md`](SYSTEM-ARCHITECTURE.md): Multi-tier architecture overview.
   - [`SERVICE-BOUNDARIES.md`](SERVICE-BOUNDARIES.md): Protocol contracts and responsibility matrix.
   - [`DATA-FLOW.md`](DATA-FLOW.md): End-to-end sequence diagrams.
   - [`DECISION-TREE-MODEL.md`](DECISION-TREE-MODEL.md): Graph invariants and JSON output format.
   - [`REFERENCE-REPOSITORY-AUDIT.md`](REFERENCE-REPOSITORY-AUDIT.md): Engineering reference audit.
2. **Requirements & Features**:
   - [`REQUIREMENT-TRACEABILITY.md`](../requirements/REQUIREMENT-TRACEABILITY.md): 30 Proposal items traced.
   - 11 Feature Specifications under `docs/features/`:
     - `FEATURE-AUTH-AND-ROLES.md`
     - `FEATURE-COURSE-AND-MATERIALS.md`
     - `FEATURE-DOCUMENT-PROCESSING-AND-RAG.md`
     - `FEATURE-CASE-GENERATION.md`
     - `FEATURE-DECISION-TREE.md`
     - `FEATURE-CASE-REVIEW-AND-PUBLISHING.md`
     - `FEATURE-CASE-SIMULATOR-AND-ARGUMENT.md`
     - `FEATURE-DEBATE-ASSISTANT.md`
     - `FEATURE-LECTURER-STATISTICS.md`
     - `FEATURE-NOTIFICATIONS.md`
     - `FEATURE-EVALUATION-AND-RESEARCH.md`
3. **Data, AI & Research**:
   - [`docs/database/DATA-MODEL.md`](../database/DATA-MODEL.md): Database schema and constraints.
   - [`docs/ai/RAG-PIPELINE.md`](../ai/RAG-PIPELINE.md): RAG pipeline & sources boundary.
   - [`docs/ai/DEBATE-ASSISTANT.md`](../ai/DEBATE-ASSISTANT.md): Socratic Devil's Advocate rules.
   - [`docs/qa/TESTING-STRATEGY.md`](../qa/TESTING-STRATEGY.md): Testing tiers and CI jobs.
   - [`docs/research/EVALUATION-DESIGN.md`](../research/EVALUATION-DESIGN.md): Classroom trial and research questions.

---

## 7. Skeleton Changes

Only minimal, justified structural and syntax corrections were made:
1. **Flyway Migration DDL Syntax Fix**: Corrected 28 instances of double single quotes (`''`) in CHECK constraints in `backend/src/main/resources/db/migration/V1__init_schema.sql` to valid standard PostgreSQL single quotes (`'`). Zero changes made to schema semantics, table names, or column structures.
2. **Resolved Broken Documentation Links**: Authored `SERVICE-BOUNDARIES.md` and `DATA-FLOW.md` to resolve broken links in `SYSTEM-ARCHITECTURE.md`.
3. **Governance Enhancement**: Updated `.github/copilot-instructions.md` with the 12 cardinal rules for future AI coding agents.
4. **README Clarification**: Updated `README.md` to prominently state that the repository is a skeleton only with no feature implementations active.

---

## 8. Feature Implementation Check

Across **all 11 feature areas and all 30 traceability items**, verified that **NONE** has business-logic implementation:

| Feature Area / Traceability Concept | Business Implementation Status | Verification Evidence |
| :--- | :---: | :--- |
| 1. Authentication & JWT Workflow | **NOT IMPLEMENTED** | User entity/schema and security filter shell exist; no registration/login controllers or token issuance services. |
| 2. User & Role Management | **NOT IMPLEMENTED** | Role enum/type exists; no user CRUD or role assignment logic implemented. |
| 3. Course Context Management | **NOT IMPLEMENTED** | Course entity/schema exists; no course creation, update, or deletion services. |
| 4. Teaching Material Upload | **NOT IMPLEMENTED** | TeachingMaterial entity/schema and MinIO bucket script exist; no upload controller or multipart streaming logic. |
| 5. Document Parsing (PDF/DOCX) | **NOT IMPLEMENTED** | Module placeholder exists; PyPDF / python-docx extraction loops are not implemented. |
| 6. Document Chunking & Embeddings | **NOT IMPLEMENTED** | `chunker.py` and provider stubs exist; no active embedding batch generation or chunk persistence. |
| 7. Vector Retrieval (RAG) | **NOT IMPLEMENTED** | pgvector schema defined; no active cosine similarity search queries or retriever classes. |
| 8. AI Case Generation (LLM) | **NOT IMPLEMENTED** | `CaseGenerationOutput` Pydantic schema exists; no active LLM prompt chain or generation endpoints. |
| 9. Decision Tree Graph Invariants | **NOT IMPLEMENTED** | BFS validator function stub exists; no database graph assembly or interactive graph editing service. |
| 10. Lecturer Review & Edit Workflow | **NOT IMPLEMENTED** | `CaseReviewPage.tsx` UI shell exists; no form submission handlers or node update endpoints. |
| 11. Case Approval & Publishing | **NOT IMPLEMENTED** | `CaseStatus` enum exists; no state transition service or publication gate queries. |
| 12. Student Interactive Simulator | **NOT IMPLEMENTED** | `BranchingCasePlayerPage.tsx` UI shell exists; no simulation navigation controller. |
| 13. Student Decision & Consequence | **NOT IMPLEMENTED** | Consequence column exists in schema; no decision evaluation or consequence delivery controller. |
| 14. Student Argument Capture | **NOT IMPLEMENTED** | Student reasoning entity exists; no argument submission or validation endpoints. |
| 15. AI Debate Assistant | **NOT IMPLEMENTED** | Challenge support session schema exists; no Socratic prompt generation or debate controller. |
| 16. Lecturer Statistics & Analytics | **NOT IMPLEMENTED** | `StatisticsPage.tsx` shell exists; no database aggregation queries or statistics endpoints. |
| 17. Notification Extension Point | **NOT IMPLEMENTED** | Package placeholder only; no email/in-app dispatch logic. |
| 18. Quantitative Research Evaluation | **NOT IMPLEMENTED** | Boundary documented; no rubric scoring endpoints or trial data export logic. |

---

## 9. Scope Violations

- **Identified**: None.
- **Excluded**: Confirmed exclusion of all K-12 specific features from `ai-teacher-copilot` (Lesson Planner, Quiz Generator, Teacher Workspace, Word Export).
- **Protection**: Prompt injection mitigation strictly documented (`<sources>` tags); autonomous AI grading strictly prohibited; AI Debate Assistant capped at 2 rounds.

---

## 10. Documentation Gaps

- All previous documentation gaps have been systematically closed:
  - Missing feature specifications → 11 dedicated specs created in `docs/features/`.
  - Missing traceability matrix → Created in `docs/requirements/REQUIREMENT-TRACEABILITY.md`.
  - Missing reference audit → Created in `docs/architecture/REFERENCE-REPOSITORY-AUDIT.md`.
  - Missing service boundaries → Created in `docs/architecture/SERVICE-BOUNDARIES.md`.
  - Missing data flows → Created in `docs/architecture/DATA-FLOW.md`.
  - Broken links in `SYSTEM-ARCHITECTURE.md` and `PROJECT_OVERVIEW.md` → Fully resolved.

---

## 11. Assumptions & Open Questions

The following candidate options and open decisions remain pending explicit Project Owner sign-off:

1. **Backend Framework Decision (DEC-01)**:
   - *Option A*: Retain current Spring Boot 3 (Java 17) scaffold.
   - *Option B*: Re-scaffold Backend Gateway to Node.js (NestJS + TypeScript) to match Proposal text.
   - *Option C*: Re-scaffold Backend Gateway to Python FastAPI to unify backend in Python.
   - *Current Stance*: Documented as candidate options in `ADR-001-TECHNOLOGY-STACK.md`. No rebuild or refactoring has been performed.
2. **Notification Channel Decision (DEC-02)**:
   - *Option A*: In-App notifications only.
   - *Option B*: Email notifications only.
   - *Option C*: Hybrid (In-App + Email).
   - *Current Stance*: Documented at Proposal level in `FEATURE-NOTIFICATIONS.md`; implementation technology is unselected.
3. **Evaluation Module Implementation Method (DEC-03)**:
   - *Option A*: In-Platform manual rubric scoring by lecturers.
   - *Option B*: Structured data export (CSV/JSON) for external statistical software analysis.
   - *Current Stance*: Marked as `Open / To Be Decided` in `FEATURE-EVALUATION-AND-RESEARCH.md`.
