---
description: Rules for student reasoning capture in Edu-Branch-AI.
trigger: keyword
keywords: [reasoning, student reasoning, justification, written response]
---

# Feature Rules: Student Reasoning Capture

## Scope
Backend Gateway (NestJS `backend/`) — `reasoning/` module.
Frontend — `pages/student/BranchingCasePlayerPage.tsx` (Reasoning Input component).

## Included
- After selecting a `CaseOption` at a Decision Point, the student submits written reasoning justifying that choice
- Reasoning is persisted to `student_reasoning`, owned strictly by `attempt_id NOT NULL` (`branching_attempts`) — NOT by the option or node globally (INV-05)
- One reasoning record per Decision Point per Attempt: `UNIQUE(attempt_id, node_id)` (INV-06)
- `selected_option_id` must belong to `node_id`'s options (service-layer validation, INV-07)
- Reasoning is the trigger for optional AI Reasoning / Challenge Support (see `feature-challenge-support.md`)
- Student may view their own submitted reasoning for their own attempts

## Excluded
- **AI grading of reasoning** — Challenge Support only asks counter-questions, never scores or grades
- **Automated pass/fail based on reasoning quality** — out of scope
- **Cross-attempt comparison/ranking** — no comparison engine (INV-18)
- Plagiarism detection — out of scope

## Service Owner
Backend Gateway (NestJS `backend/`) — `reasoning/` module.

## Constraints
- Reasoning text should have a minimum length (10 chars) and maximum length (2000 chars)
- Reasoning is stored as plain text (no HTML, sanitize on input)
- `studentId` is always derived from JWT via the owning `attempt` — never trust a client-provided student ID
- Retrying a case creates a NEW `branching_attempts` row; a new attempt means new reasoning rows, even for the same option chosen again — past attempts and their reasoning are immutable (INV-12)

## Testing Expectations
- Test reasoning length validation
- Test that a student cannot submit reasoning for another student's attempt
- Test `UNIQUE(attempt_id, node_id)` is enforced (one reasoning row per Decision Point per Attempt)
