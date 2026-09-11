# Contributing to EduBranch AI

> Applies to all development on **EduBranch AI — AI Platform for Interactive Branching Case Studies and Open Review in University Teaching**.
> All code changes must comply with these standards before being integrated into `develop` or `main`.

---

## 🌳 1. Git Branching Strategy

EduBranch AI uses **Git Feature Branch Workflow**. **Never** push code directly to `main` or `develop`.

```
feature/<name>  →  develop  →  main
```

| Branch | Description |
| :--- | :--- |
| `main` | Stable / release branch. Must remain clean and release-ready at all times. |
| `develop` | Integration branch. Receives merges from `feature/*` after CI passes. |
| `feature/*` | Feature development. Created from `develop`, merged back via PR. |
| `fix/*` | Bug fixes during development. |
| `hotfix/*` | Emergency fixes applied directly from `main`. |
| `refactor/*` | Code restructuring without adding features. |
| `docs/*` | Documentation updates. |

### Branch Naming

| Type | Pattern | Example |
| :--- | :--- | :--- |
| Feature | `feature/<module>-<short-name>` | `feature/rag-case-generator` |
| Bug fix | `fix/<module>-<description>` | `fix/simulation-node-traversal` |
| Hotfix | `hotfix/<description>` | `hotfix/jwt-expiry` |
| Refactor | `refactor/<module>` | `refactor/debate-assistant-api` |
| Docs | `docs/<topic>` | `docs/decision-tree-model` |

---

## 📝 2. Commit Convention (Conventional Commits)

Every commit message must follow:

```
<type>(<scope>): <short description>
```

**Scopes:** `backend` · `ai-service` · `frontend` · `infra` · `docs`

| Type | Purpose | Example |
| :--- | :--- | :--- |
| `feat` | Add new feature | `feat(ai-service): add structured case generation with JSON schema` |
| `fix` | Fix a bug | `fix(backend): fix DRAFT→APPROVED status transition validation` |
| `docs` | Documentation update | `docs: update RAG pipeline architecture diagram` |
| `style` | Code formatting (no logic change) | `style(frontend): apply prettier formatting` |
| `refactor` | Code restructuring | `refactor(ai-service): optimize pgvector retrieval query` |
| `test` | Add or fix tests | `test(backend): add simulation session integration test` |
| `chore` | Library updates, config | `chore: upgrade nestjs to 10.x` |
| `ci` | CI/CD workflow changes | `ci: add ai-service pytest job to github actions` |

---

## 🎨 3. Code Formatting Standards

### A. Frontend — React 19 + TypeScript + Vite

**Naming conventions:**
- Components & Component files: `PascalCase` → `CaseSimulator.tsx`, `DebatePanel.tsx`
- Custom hooks: `camelCase` starting with `use` → `useSimulation.ts`, `useDebate.ts`
- Utils / Services / Stores: `camelCase` → `apiClient.ts`, `authStore.ts`

**Component architecture:**
- Use **Functional Components** with clear TypeScript Interfaces/Types
- Never write API call logic directly in UI components — consolidate in `src/services/`
- Global state management via **Zustand** (`src/stores/`)
- Centralized Axios client with JWT interceptors at `src/services/apiClient.ts`
- **Never** store secrets or API keys in frontend environment variables

### B. Backend Gateway — Node.js 20 + NestJS 10 + TypeScript

**Module architecture:**
```
Controller → Service (Interface + Impl) → Repository → Entity / DTO
```

**Rules:**
- Mandatory use of **DTO** (Data Transfer Objects) with `class-validator` when receiving and returning API data
- **Never** expose raw database entities directly in REST responses
- Module by feature/domain: `auth/`, `user/`, `course/`, `material/`, `case/`, `simulation/`, `argument/`, `debate/`, `statistics/`, `evaluation/`, `notification/`, `common/`
- Use NestJS Guards for authentication/authorization enforcement
- Use NestJS Interceptors for response transformation and logging

### C. AI Service — Python 3.12 + FastAPI

**Rules:**
- Package by domain: `core/`, `providers/`, `ingestion/`, `retrieval/`, `generation/`, `debate/`, `evaluation/`
- **Always** use provider abstraction (`providers/base.py`) — never hardcode vendor-specific SDK logic in route handlers
- Pydantic v2 models for all: request schemas, response schemas, structured AI outputs
- Retrieved document content is **untrusted data** — always wrap in `<sources>...</sources>` boundary before passing to LLM

---

## 🔄 4. Pull Request Process

### Before Opening a PR

- [ ] Branch is created from `develop` (not `main`)
- [ ] Branch name follows naming convention
- [ ] All commits follow the commit convention
- [ ] Code is formatted and linted
- [ ] Tests pass locally
- [ ] No secrets, API keys, or `.env` files committed
- [ ] Documentation updated if required

### PR Requirements

- **Title**: `<type>(<scope>): <description>` — same as commit convention
- **Description**: Use the PR template (`.github/pull_request_template.md`)
- **CI must pass**: All GitHub Actions checks must be green before merging
- **Review**: At least one approval required before merging to `develop`
- **Merge**: Squash merge or merge commit — no direct push to `develop` or `main`

---

## 🏗️ 5. Architecture Boundaries — DO NOT VIOLATE

| Rule | Details |
| :--- | :--- |
| Frontend → Backend Gateway only | React never calls the AI Service directly |
| AI Service is internal | The AI Service is not exposed to the public internet |
| Untrusted document content | Retrieved chunks MUST be wrapped in `<sources>...</sources>` |
| Human-in-the-loop mandatory | Cases start as DRAFT; lecturer must APPROVE before publication |
| AI does not grade | The Debate Assistant generates counter-questions only; never grades or decides pass/fail |
| Own your domain | Never leak Backend Gateway business logic into the AI Service, and vice versa |

---

## 🔒 6. Security Rules

- **Never** commit `.env` files or actual secrets
- **Never** hardcode API keys, passwords, or connection strings in source code
- **Never** expose internal service URLs or secret keys in API responses
- **Always** validate file uploads (type, size, content)
- **Always** enforce authorization checks at the Backend Gateway (NestJS) layer
- **Always** enable the pre-commit safeguard hook locally: `git config core.hooksPath .githooks`
- See [SECURITY.md](SECURITY.md) for the full security policy
