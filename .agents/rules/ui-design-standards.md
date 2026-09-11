---
description: Rules for UI/UX implementation in EduBranch AI.
trigger: always_on
---

# Feature Rules: UI/UX Design Standards

## 1. Core Mandate

EduBranch AI is a university-level professional tool.
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

### Lecturer Pages
- `/lecturer/courses` — course list and creation
- `/lecturer/courses/:courseId/materials` — material upload and status
- `/lecturer/courses/:courseId/cases` — case list, trigger generation
- `/lecturer/cases/:caseId/review` — decision tree review (ReactFlow), edit, approve, publish
- `/lecturer/statistics` — simple participation and branch statistics

### Student Pages
- `/student/cases/:caseId/simulate` — decision-tree navigator
- `/student/cases/:caseId/debate/:sessionId` — debate interface (argument + AI counter-question)

## 6. Decision Tree Visualization

- Use ReactFlow for interactive decision tree display in case-review and simulator
- Nodes represent `CaseNode` (situation)
- Edges represent `CaseOption` (decision + consequence)
- Lecturer view: editable, node click opens edit panel
- Student view: read-only navigation, highlight current node

## 7. Security

- **Never display** internal IDs, database keys, or server error details to users
- **Never store** API keys, JWT secrets, or credentials in frontend env vars
- Always validate forms client-side AND server-side
