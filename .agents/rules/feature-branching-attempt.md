---
description: Rules for the Branching Case Player and branching attempt/retry model in Edu-Branch-AI.
trigger: keyword
keywords: [branching attempt, branching case player, branching study, student, decision, node, consequence, navigate, case play, retry]
---

# Feature Rules: Branching Case Player & Branching Attempt Model

## Scope
Backend Gateway (NestJS `backend/`) — `branching-attempt/` module.
Frontend — `pages/student/BranchingCasePlayerPage.tsx` (ReactFlow-adjacent read-only player, not the lecturer's editor).

## Included
- Student loads a `PUBLISHED` case with `learning_mode = 'BRANCHING_STUDY'`
- Student sees the current situation (`CaseNode`) and its available `CaseOption` choices
- Student selects an option, submits required reasoning (see `feature-reasoning.md`), then sees the lecturer-authored `consequence`
- System advances the attempt to `option.next_node_id`
- System detects terminal node (`is_terminal = TRUE`) and records `outcome_node_id`, `is_completed = TRUE`
- Attempt state persisted: `attempt_number`, `current_node_id`, `outcome_node_id`, `is_completed`, `reflection_text`, `reflection_status`
- Student may retry: a retry creates a NEW `branching_attempts` row with `attempt_number = previous + 1` (`UNIQUE(student_id, case_id, attempt_number)`)
- Past attempts are immutable history — never overwritten or mutated retrospectively

## Excluded
- Student modifying the case or its content (nodes/options/consequences are lecturer-owned)
- Skipping nodes or options
- Real-time multi-student interaction in the same attempt
- **No Comparison Engine**: no automated semantic diffs, ranking, or auto-comparison across attempts
- **No Attempt Scoring**: no scoring columns on `branching_attempts`, no grading of the path taken

## Service Owner
Backend Gateway: attempt persistence, node traversal logic, retry/versioning.
Frontend: Branching Case Player UI (situation/option/consequence display, reasoning capture handoff, outcome/reflection handoff).

## Constraints
- Only `PUBLISHED` cases can be loaded (`INV-01`)
- `studentId` is always set from JWT — never trust a client-provided student ID
- Terminal node detection is based on `CaseNode.is_terminal`
- `reflection_status` defaults to `NOT_STARTED`, transitions to `SUBMITTED` only via the Reflection screen (see `feature-course.md`/reflection handling, tracked on `branching_attempts`)

## Testing Expectations
- Test that non-`PUBLISHED` cases return 403/404
- Test attempt creation and node progression
- Test terminal node detection and `outcome_node_id` recording
- Test that retry creates a new attempt row rather than mutating the previous one, and that `attempt_number` increments correctly
