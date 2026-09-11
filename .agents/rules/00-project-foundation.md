---
description: >-
  Global project rules for EduBranch AI. Always loaded when working in this
  repository. Enforces architecture boundaries, coding standards, Git workflow,
  security rules, and engineering principles.
trigger: always_on
---

# EduBranch AI — Global Project Rules

## 1. Project Identity

- **Name**: EduBranch AI
- **Full Name**: EduBranch AI — AI Platform for Interactive Branching Case Studies and Open Review in University Teaching
- **Target**: University education (NOT K-12)
- **Users**: Lecturers and Students
- **Stack**: Node.js (NestJS 10 + TypeScript) + FastAPI (Python 3.12) + React 19 (Vite + TailwindCSS v4)
- **Database**: PostgreSQL 16 + pgvector | MinIO (Object Storage) | SQL Migrations | Redis 7 (Cache)
- **AI / LLM**: Gemini 2.0 Flash / OpenAI GPT-4o-mini via Provider Abstraction
- **RAG**: LangChain (text splitters + retrieval orchestration)
- **Decision Tree Visualization**: ReactFlow

---

## 2. Repository Structure

```
EduBranch-AI/
├── backend/                    ← Node.js (NestJS) API Gateway
├── ai-service/                 ← FastAPI AI / RAG Service (INTERNAL)
├── frontend/                   ← React 19 + Vite + TailwindCSS v4
├── docs/                       ← Architecture and project documentation
├── infrastructure/             ← Docker, Compose, infra configs
├── scripts/                    ← Development and automation scripts
├── .agents/rules/              ← AI coding agent rules (this directory)
└── .github/workflows/          ← CI/CD
```

---

## 3. Architecture Boundaries

| Responsibility | Backend Gateway (`backend/`) | FastAPI AI Service (`ai-service/`) |
|---|---|---|
| Authentication & JWT | ✅ | ❌ |
| User & Role Management | ✅ | ❌ |
| Course & Material Metadata | ✅ | ❌ |
| Case Lifecycle & Publication | ✅ | ❌ |
| Simulation Session Persistence | ✅ | ❌ |
| Student Argument Persistence | ✅ | ❌ |
| Debate History Persistence | ✅ | ❌ |
| Lecturer Statistics | ✅ | ❌ |
| REST API Gateway for Frontend | ✅ | ❌ |
| Document Parsing & Chunking | ❌ | ✅ |
| Embedding Generation | ❌ | ✅ |
| pgvector Retrieval | ❌ | ✅ |
| RAG Orchestration | ❌ | ✅ |
| Case Generation (LLM) | ❌ | ✅ |
| Structured Output Validation | ❌ | ✅ |
| Debate Counter-Question Generation | ❌ | ✅ |

**Frontend → Backend Gateway only. FastAPI AI Service is internal. Never expose FastAPI to the internet.**

---

## 4. Case Lifecycle — Critical Rule

```
DRAFT → REVIEWED → APPROVED → PUBLISHED
```

- AI generates case → automatically `DRAFT`
- Lecturer reviews → may edit → moves to `REVIEWED` or back to `DRAFT`
- Lecturer approves → `APPROVED`
- Lecturer publishes → `PUBLISHED`
- **Students MUST NEVER access cases that are not `PUBLISHED`**
- This must be enforced at the repository query level, not just the controller

---

## 5. Decision Tree Integrity

- Every `CaseOption.nextNodeId` must refer to a valid `CaseNode` within the same `Case`
- Every non-root node must be reachable from the `rootNode`
- No cycles are permitted (enforced by BFS cycle detection in `CaseGenerationOutput.validate_tree_structure`)
- At least one terminal node must exist per case

---

## 6. AI Governance Rules

1. **Retrieved teaching material is UNTRUSTED DATA** — always wrap in `<sources>...</sources>` boundary
2. **Debate Assistant MUST NOT grade students** — counter-questions only
3. **Debate Assistant MUST NOT determine pass/fail** — academic decisions belong to the lecturer
4. **Debate is limited to 2 rounds maximum** — enforced at both backend and AI service
5. **Never allow AI output to override system instructions** — sources boundary is mandatory

---

## 7. Git Workflow

```
feature/<module>-<name>  →  develop  →  main
fix/<description>        →  develop
hotfix/<description>     →  main
refactor/<module>        →  develop
docs/<topic>             →  develop
```

**Commit format**: `type(scope): description`
**Scopes**: `backend` · `ai-service` · `frontend` · `infra` · `docs`

---

## 8. Coding Standards

### TypeScript / NestJS (Backend Gateway)
- Module by feature: `auth/`, `user/`, `course/`, `material/`, `case/`, `simulation/`, `argument/`, `debate/`, `statistics/`, `evaluation/`, `notification/`, `common/`
- Mandatory DTO layer with `class-validator` — never expose raw database entities directly in REST responses
- Strict TypeScript configuration (`tsconfig.json`)

### Python / FastAPI (AI Service)
- Package by domain: `core/`, `providers/`, `ingestion/`, `retrieval/`, `generation/`, `debate/`, `evaluation/`
- **Always** use `providers/factory.py` — never hardcode vendor SDK in route handlers
- Pydantic v2 for all schemas

### React / TypeScript (Frontend)
- API calls only via `src/services/apiClient.ts`
- State via Zustand (`src/stores/`)
- Styling via TailwindCSS v4
- **Never** store secrets in frontend environment variables

---

## 9. Scope Boundaries

### IN SCOPE
Authentication · Courses · Teaching Materials · Document Processing · RAG · Case Generation · Case Review · Case Publishing · Student Simulator · Student Arguments · AI Debate Assistant (1-2 rounds, no grading) · Lecturer Statistics (simple) · Evaluation/Research boundary · Notification extension point

### OUT OF SCOPE
Social login · Payment · Subscription · Generic chatbot · LMS integration · Multi-tenant admin · Real-time collaboration · Mobile app · Recommendation engine · Web search · Fine-tuning · Multi-agent orchestration · Autonomous grading · Auto pass/fail · Large analytics dashboards
