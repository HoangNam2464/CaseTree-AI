# Engineering Reference Repository Audit: ai-teacher-copilot

> **Document Status**: Authoritative Engineering Audit  
> **Source Reference Repository**: `https://github.com/HoangNam2464/ai-teacher-copilot` (`D:\DU_AN_2026\Python\ai-teacher-copilot`)  
> **Target System**: **Edu-Branch-AI — AI Platform for Interactive Branching Case Studies and Open Review in University Teaching**  
> **Mandate**: This document classifies the engineering practices, architectural patterns, and governance rules of the reference repository. Under no circumstances may source code, business domain logic, or K-12 product features from the reference repository be copied into Edu-Branch-AI.

---

## 1. Audit Classification Matrix

Every inspected file or pattern from `ai-teacher-copilot` is classified under one of five strict categories:

1. **`REUSABLE ENGINEERING RULE`**: Process, formatting, commit, branching, PR, or security rules adopted for Edu-Branch-AI.
2. **`REUSABLE ARCHITECTURAL PATTERN`**: Service boundaries, internal token isolation, or retrieval abstractions adapted to Edu-Branch-AI.
3. **`REFERENCE ONLY`**: Contextual examples, prompt ideas, or educational references that provide background only.
4. **`NOT APPLICABLE`**: Specific to K-12 teaching, lesson plans, exam generation, or features not in Edu-Branch-AI scope.
5. **`REQUIRES ADAPTATION`**: Useful concept that must be altered to fit university-level case studies and decision trees.

---

## 2. File-by-File Reference Audit Table

| Reference File / Asset | Original Purpose in `ai-teacher-copilot` | Classification | Edu-Branch-AI Adaptation & Disposition |
| :--- | :--- | :--- | :--- |
| **`CONTRIBUTING.md`** | Development guidelines, Git Feature Branch strategy, Conventional Commits, code standards. | **`REUSABLE ENGINEERING RULE`** | **Adopted**: Feature branch workflow (`feature/* → develop → main`), conventional commit types (`feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `ci`), and PR review requirements adopted directly in `CONTRIBUTING.md`. Scope names tailored to `backend`, `ai-service`, `frontend`, `infra`, `docs`. |
| **`SECURITY.md`** | Security policies, JWT auth, internal service token, untrusted document handling. | **`REUSABLE ENGINEERING RULE`** | **Adopted**: Mandatory secret management (no `.env` committed), internal FastAPI isolation (`X-Internal-API-Key`), BCrypt password hashing, and `<sources>...</sources>` untrusted data boundary adopted in Edu-Branch-AI `SECURITY.md`. |
| **`.github/pull_request_template.md`** | PR checklist, test verification, security review. | **`REUSABLE ENGINEERING RULE`** | **Adopted**: Adapted PR checklist requiring linting, test pass verification, no hardcoded credentials, and service boundary adherence. |
| **`.github/copilot-instructions.md`** | Instructions for AI coding assistants on project boundaries and stack. | **`REUSABLE ENGINEERING RULE`** | **Adapted**: Formulated CaseTree-specific instructions emphasizing the Proposal as source of truth, human-in-the-loop review, decision-tree integrity, and anti-hallucination guardrails. |
| **`docs/Guardrails.md`** | UI composition budgets, anti-clutter rules, screen categorization (Action vs. Workspace). | **`REQUIRES ADAPTATION`** | **Adapted**: Adapted into `.agents/rules/ui-design-standards.md` to prevent visual clutter, ban fake AI avatars/typing animations, and standardize university-level UI with TailwindCSS. |
| **`docker-compose.yml` / `docker-compose.full.yml`** | Docker configuration for local Postgres, Redis, MinIO, and app services. | **`REUSABLE ARCHITECTURAL PATTERN`** | **Adopted**: Local dev infrastructure isolates PostgreSQL 16 + pgvector, Redis 7, and MinIO object storage. Application services run locally for hot reload. |
| **`ai-service/app/providers/` (`base.py`, `factory.py`)** | LLM provider abstraction layer isolating vendor SDKs (Gemini, OpenAI). | **`REUSABLE ARCHITECTURAL PATTERN`** | **Adopted**: Provider interface pattern adopted to allow swapping between Gemini 2.0 Flash and OpenAI GPT-4o-mini without rewriting route or RAG logic. |
| **`ai-service/app/ingestion/`** | PDF/DOCX parsing, chunking, and metadata extraction. | **`REUSABLE ARCHITECTURAL PATTERN`** | **Adapted**: Chunking and parsing pipelines adapted for university course syllabus, lecture slides, and case notes. LangChain text splitters utilized as an allowed/possible option. |
| **`ai-service/app/retrieval/`** | Cosine similarity query over pgvector embeddings. | **`REUSABLE ARCHITECTURAL PATTERN`** | **Adopted**: pgvector HNSW/IVFFlat index querying with course-level and material-level metadata filtering adopted for case retrieval. |
| **`docs/01_MASTER-TASKS.md` & `02_SPRINT-TASKS.md`** | Jira task breakdown and sprint backlog for K-12 Teacher Copilot. | **`NOT APPLICABLE`** | **Excluded**: Specific to K-12 lesson planning tasks. Edu-Branch-AI tasks are derived strictly from the Edu-Branch-AI Proposal (C1SE.65). |
| **`.agents/rules/feature-lesson-planner.md`** | Rules for generating K-12 lesson plans with Bloom's taxonomy. | **`NOT APPLICABLE`** | **Excluded**: Lesson Planner is strictly out of scope for Edu-Branch-AI. |
| **`.agents/rules/feature-quiz-generator.md`** | Rules for generating multiple-choice quizzes and exams. | **`NOT APPLICABLE`** | **Excluded**: Exam/Quiz Generator is strictly out of scope for Edu-Branch-AI. |
| **`.agents/rules/feature-workspace.md`** | Rules for teacher document workspace and folders. | **`NOT APPLICABLE`** | **Excluded**: Replaced by Edu-Branch-AI Course & Material context model. |
| **`.agents/rules/feature-export.md`** | Rules for exporting lesson plans to DOCX/PDF via python-docx. | **`NOT APPLICABLE`** | **Excluded**: Exporting lesson plans is not in Edu-Branch-AI MVP scope. |
| **`backend/` (Spring Boot 3 Implementation)** | Domain entities and business logic for teacher workspaces and quizzes. | **`NOT APPLICABLE`** | **Excluded / Replaced**: Reference implementation code must not be copied. In Edu-Branch-AI, the Backend Gateway is ratified as Node.js (NestJS 10 + TypeScript) per Proposal Sections 7 & 11. The inherited Spring Boot scaffold has been removed. |
| **`frontend/` (React + Tailwind Pages)** | UI components for lesson planning, quiz card editing, and teacher dashboard. | **`NOT APPLICABLE`** | **Excluded**: Edu-Branch-AI requires custom UI for Case Review (ReactFlow decision tree), Student Simulator, and Debate Assistant. |
| **`docs/ENGINEERING_KNOWLEDGE.md`** | Technical patterns for JPA, Flyway, Redis caching, and Pydantic validation. | **`REUSABLE ENGINEERING RULE`** | **Adopted**: Pydantic v2 validation for structured JSON, layered service architecture, and Flyway migration practices adopted for Edu-Branch-AI documentation. |

---

## 3. Reference Features Explicitly Excluded

To protect project identity and prevent scope expansion, the following `ai-teacher-copilot` features are **permanently excluded** from Edu-Branch-AI:

1. **Lesson Planner**: No lesson plan drafting, unit templates, or weekly schedules.
2. **Quiz / Exam Generator**: No multiple-choice question generation, answer key generation, or exam paper layout.
3. **Teacher Workspace / Personal Drive**: No generic personal cloud folder or file management.
4. **Word Document Export**: No DOCX export pipeline for lesson plans.
5. **Bloom's Taxonomy Calibration**: No classification of quiz questions into Bloom cognitive levels.
6. **Autonomous Rubric-Based Grading**: No automated scoring of student essays or pass/fail decisions.

---

## 4. Reusable Engineering Patterns Adopted

The following high-value engineering patterns from `ai-teacher-copilot` are adopted in Edu-Branch-AI:

1. **Strict 3-Tier Boundary**: `Frontend (Browser) → Backend (Gateway & Persistence) → AI Service (Internal Reasoning & RAG)`.
2. **Untrusted Data Boundary**: Every piece of retrieved teaching material chunk text is enclosed inside `<sources>...</sources>` tags before being passed to LLMs to prevent indirect prompt injection.
3. **Provider Factory**: `providers/factory.py` ensures that LLM provider instantiation is decoupled from business logic and route handlers.
4. **Health Check Probes**: Both backend and internal AI service expose unauthenticated `/health` endpoints for container orchestration readiness/liveness checks.
5. **Convention Over Configuration**: Strict adherence to Conventional Commits and feature-based branch naming.
