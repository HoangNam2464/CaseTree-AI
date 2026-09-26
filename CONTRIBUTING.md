# Contributing to Edu-Branch-AI

> Applies to all development on **Edu-Branch-AI — AI Platform for Experiential Case-Based Learning in University Teaching**.
> All code changes must comply with these standards before being integrated into `develop` or `main`.

---

## 🌿 1. Git Branching Strategy

Edu-Branch-AI uses **Git Feature Branch Workflow**. **Never** push code directly to `main` or `develop`.

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
| Bug fix | `fix/<module>-<description>` | `fix/branching-node-traversal` |
| Hotfix | `hotfix/<description>` | `hotfix/jwt-expiry` |
| Refactor | `refactor/<module>` | `refactor/challenge-support-api` |
| Docs | `docs/<topic>` | `docs/branching-study-review-phase` |

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
| `test` | Add or fix tests | `test(backend): add branching attempt integration test` |
| `chore` | Library updates, config | `chore: upgrade nestjs to 10.x` |
| `ci` | CI/CD workflow changes | `ci: add ai-service pytest job to github actions` |

---

## 🎨 3. Code Formatting Standards

### A. Frontend — React 19 + TypeScript + Vite

**Naming conventions:**
- Components & Component files: `PascalCase` → `BranchingCasePlayerPage.tsx`, `BranchingReviewPage.tsx`
- Custom hooks: `camelCase` starting with `use` → `useBranchingAttempt.ts`, `useReviewJourney.ts`
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
- Module by feature/domain: `auth/`, `user/`, `course/`, `material/`, `case/`, `branching-attempt/`, `reasoning/`, `challenge-support/`, `review-study/`, `lecturer-feedback/`, `statistics/`, `evaluation/`, `notification/`, `common/`
- Use NestJS Guards for authentication/authorization enforcement
- Use NestJS Interceptors for response transformation and logging

### C. AI Service — Python 3.12 + FastAPI

**Rules:**
- Package by domain: `core/`, `providers/`, `ingestion/`, `retrieval/`, `generation/`, `challenge_support/`, `evaluation/`
- **Always** use provider abstraction (`providers/factory.py`) — never hardcode vendor-specific SDK logic in route handlers
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
| AI does not grade | The AI Reasoning / Challenge Support generates Socratic counter-questions only; never grades, scores, or decides pass/fail |
| AI does not alter approved cases | AI must never change branch structures, consequences, or outcomes after Lecturer approval |
| Experience-first in Branching Study | No reasoning form, no consequence card, no blocking step between consecutive Decision Points during the Experience phase |
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
