---
description: Rules for UI/UX implementation in CaseTree AI.
trigger: always_on
---

# Feature Rules: UI/UX Design Standards

## 1. Core Mandate

CaseTree AI is a university-level professional tool.
UI must be: **simple, clean, functional, and consistent.**

## 2. Technology Stack

- **React 19 + Vite + TypeScript**
- **TailwindCSS v4** for all styling
- **ReactFlow** for decision tree visualization
- **Zustand** for state management
- **Axios** (via centralized apiClient) for HTTP calls

## 3. Anti-Clutter Rules

1. **No unnecessary decorative elements** — every UI element must serve a function
2. **No excessive explanatory text** — labels must be concise and self-explanatory
3. **No "AI-looking" clutter** — no typing animations, no AI avatar faces, no gimmicks
4. **Consistent spacing** — follow TailwindCSS spacing scale (4, 8, 12, 16, 24, 32)
5. **Consistent colors** — use the TailwindCSS color palette, avoid arbitrary hex values

## 4. Component Rules

- Components in `src/components/` are reusable and presentational only
- Business logic stays in services (`src/services/`) or feature directories
- Never write API calls inside component files
- Props must have explicit TypeScript types

## 5. Page Structure by User Role

> Route list mirrors the live `frontend/src/app/router.tsx` (see `docs/design/GLOBAL-DESIGN-SYSTEM.md` and `docs/design/screens/` for full per-screen specs).

### Lecturer Pages
- `/lecturer/courses` — course list and creation
- `/lecturer/courses/:courseId/materials` — material upload and status
- `/lecturer/courses/:courseId/cases` — case list, filter by learning mode, trigger AI case generation
- `/lecturer/cases/:caseId/review` — decision tree review (ReactFlow) for Branching Study / form editor for Review Study — edit, approve, publish
- `/lecturer/cases/:caseId/feedback` — review student Review Study submissions / Branching Study attempts, write lecturer feedback
- `/lecturer/statistics` — simple participation and branch statistics

### Student Pages
- `/student/cases/:caseId/branching-play` — Branching Case Player (situation → options → reasoning → consequence → next node → outcome)
- `/student/cases/:caseId/attempt/:attemptId/reflect` — post-outcome reflection
- `/student/cases/:caseId/challenge/:sessionId` — AI Reasoning / Challenge Support (max 2 rounds; supports both Branching Study and Review Study targets)
- `/student/cases/:caseId/review-study` — Review Study case analysis, proposed solution, and reasoning
- `/student/cases/:caseId/review-study/:submissionId/feedback` — lecturer feedback + reflection for a Review Study submission

## 6. Decision Tree Visualization

- Use ReactFlow for interactive decision tree display in Case Review (lecturer, editable) and the Branching Case Player (student, read-only navigation)
- Nodes represent `CaseNode` (situation)
- Edges represent `CaseOption` (decision + consequence)
- Lecturer view: editable, node click opens edit panel
- Student view: read-only navigation, highlight current node

## 7. Security

- **Never display** internal IDs, database keys, or server error details to users
- **Never store** API keys, JWT secrets, or credentials in frontend env vars
- Always validate forms client-side AND server-side
