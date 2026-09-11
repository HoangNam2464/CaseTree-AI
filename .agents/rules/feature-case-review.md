---
description: Rules for lecturer case review, edit, and publication workflow in EduBranch AI.
trigger: keyword
keywords: [case review, approve, publish, edit case, case lifecycle, draft, approved, published]
---

# Feature Rules: Lecturer Review & Edit

## Scope
Backend Gateway (NestJS `backend/`) — `case/` module.
Frontend — `features/case-review/`.

## Included
- Lecturer sees generated case in DRAFT status
- Lecturer can inspect all nodes and options
- Lecturer can edit case title, description, node situations, option text, consequence
- Lifecycle transitions: DRAFT → REVIEWED → APPROVED → PUBLISHED
- Version increment on each significant edit
- Basic version/history support

## Excluded
- Real-time collaboration editing — out of scope
- AI auto-regeneration of specific nodes without lecturer request — out of scope
- Automatic approval — human-in-the-loop is mandatory

## Service Owner
Backend Gateway (NestJS) — enforces lifecycle transitions
Frontend — case tree visualization (ReactFlow) and edit UI

## Constraints
- **STUDENTS MUST NEVER SEE CASES THAT ARE NOT PUBLISHED**
- This check must be at the repository query level
- A case can only transition forward in the lifecycle (DRAFT→REVIEWED→APPROVED→PUBLISHED)
- Rollback to DRAFT is allowed for editing
- Published cases cannot be edited (must unpublish first → create new version)

## Testing Expectations
- Status transition tests (valid and invalid transitions)
- Confirm student endpoint returns 404 for non-PUBLISHED cases
- Confirm lecturer can edit only their own courses'' cases
