# P4 — Secondary Review Study (LATER)

> **Priority**: LATER — Proposal V1.1 explicitly calls Review Study "supported at a simple level in the MVP," lowest build priority. Lighter-pass spec per Phase 2 plan.
> **Visual system**: `docs/design/GLOBAL-DESIGN-SYSTEM.md`.
> **Covers**: `/student/cases/:caseId/review-study`, `/student/cases/:caseId/review-study/:submissionId/feedback`.

---

## 1. Review Study (`/student/cases/:caseId/review-study`)

### Purpose & Function
Context/Data → Problem/Question → Student Analysis → Proposed Solution → Student Reasoning, for cases with `learning_mode = REVIEW_STUDY` (`FEATURE-REVIEW-STUDY.md`). No decision tree — `context_text`/`problem_text` only.

### Layout
Single-column reading + writing flow, same capped-width readable column as the Branching Case Player: `context_text` → `problem_text` → an optional `student_analysis` field → `proposed_solution` (required) → `reasoning_text` (required), using the Reasoning Input pattern (`GLOBAL-DESIGN-SYSTEM.md §6.6`) for the reasoning field specifically.

### Data
`context_text`, `problem_text` (from the case), `student_analysis`, `proposed_solution`, `reasoning_text` (student-authored, `review_study_submissions`).

### Actions
- Submit → creates the single `review_study_submissions` row for this (student, case) pair (`submission_status = SUBMITTED`).
- Optional: open Challenge Support on the submitted `proposed_solution`/`reasoning_text` (same panel as `P2-student-core.md §3`, targeting `review_submission_id` instead of a `reasoning_id`).

### States
- **Already submitted**: read-only view of what was submitted — **no retry/resubmit affordance** (`FEATURE-REVIEW-STUDY.md §3`: "Exactly one submission... no retry / re-submission").

### Boundary
No AI grading of `proposed_solution` or `reasoning_text`. No "correct answer" framing anywhere — the feature doc is explicit that multiple valid perspectives exist and the system never determines a single correct answer (`§1` Fundamental Principle).

---

## 2. Review Feedback (`/student/cases/:caseId/review-study/:submissionId/feedback`)

### Purpose & Function
Student view of the Lecturer's feedback on their Review Study submission, and the entry point to submit a reflection (`FEATURE-LECTURER-FEEDBACK.md §3`, `FEATURE-REFLECTION.md`).

### Layout
Read-only recap of the student's own `proposed_solution`/`reasoning_text` → Lecturer Feedback Block (`GLOBAL-DESIGN-SYSTEM.md §6.10`) → Reflection Input (`§6.8`), shown only once `submission_status = REVIEWED`.

### States
- **Not yet reviewed**: if the lecturer hasn't submitted feedback yet, show a waiting state ("Your lecturer hasn't reviewed this submission yet") rather than an empty feedback block.
- **Already reflected**: read-only, matching the Reflection screen's already-submitted state pattern (`P2-student-core.md §2`).

### Boundary
Same as `P2-student-core.md §2` — no AI grading/scoring of the reflection.
