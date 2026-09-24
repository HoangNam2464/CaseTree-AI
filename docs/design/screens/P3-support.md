# P3 — Support & Statistics (LATER)

> **Priority**: LATER — important, not blocking the Branching-Study-focused MVP classroom trial. Lighter-pass spec per Phase 2 plan; deepen when this priority tier is actually scheduled for build.
> **Visual system**: `docs/design/GLOBAL-DESIGN-SYSTEM.md`.
> **Covers**: `/lecturer/statistics`, `/lecturer/cases/:caseId/feedback`.

---

## 1. Lecturer Statistics (`/lecturer/statistics`)

### Purpose & Function
Surfaces the five Proposal-defined Learning-Flow metrics: completion, selected branch distribution, number of attempts, outcome distribution, learning-flow status (`FEATURE-BASIC-STATISTICS.md`).

### User & Context
Lecturer only. Entered from the top-level nav or a "View Statistics" link on a specific case.

### Layout
Case selector (if not arriving scoped to one case) → summary number cards (completion rate, total attempts, single-attempt vs. retry split) using the Statistics Widgets component (`GLOBAL-DESIGN-SYSTEM.md §6.12`) → a branch-selection-distribution breakdown per Decision Point → a learning-flow status breakdown (in-progress / completed / reflected for Branching; submitted / reviewed / reflected for Review Study).

### Data
Sourced from `branching_attempts` (`is_completed`, `attempt_number`, `outcome_node_id`, `reflection_status`), `student_reasoning` (`selected_option_id`, `node_id`), `review_study_submissions` (`submission_status`, `reflection_status`).

### States
- **Empty**: "No attempts yet" if a case has zero student activity.
- **Loading**: skeleton number cards + skeleton bars.

### Boundary
Strictly the 5 defined metrics — no comparison/ranking engine, no scoring, no predictive modeling, no cross-course analytics dashboard (`FEATURE-BASIC-STATISTICS.md §3`). This is the only screen where aggregate student data is shown across a cohort; it must never surface an individual student's reasoning text here — that belongs on the Lecturer Feedback screen (§2) or Case Review, not the statistics aggregate view.

---

## 2. Lecturer Feedback (`/lecturer/cases/:caseId/feedback`)

### Purpose & Function
Lets the Lecturer review individual student Review-Study submissions (and, per `FEATURE-LECTURER-FEEDBACK.md §1`, individual Branching Study attempts) and author qualitative feedback (`FEATURE-LECTURER-FEEDBACK.md`).

### Layout
List of student submissions/attempts for the case (filterable by status: submitted / reviewed / reflected) → selecting one opens the Review-Study Submission Card (`GLOBAL-DESIGN-SYSTEM.md §6.9`) or an equivalent read view of a Branching attempt's path/reasoning → a Lecturer Feedback Block (`§6.10`) with a textarea to author `feedback_text`.

### Data
`branching_attempt_id` or `review_submission_id` (exactly one per feedback record — `chk_feedback_one_target`), `feedback_text`.

### Actions
- Submit feedback → creates/updates the `lecturer_feedback` row; for Review Study this transitions `submission_status` from `SUBMITTED` to `REVIEWED`, unlocking the student's reflection step (`FEATURE-LECTURER-FEEDBACK.md §3`).

### Boundary
No AI-generated feedback suggestions and no grade/score field anywhere on this screen — feedback is 100% lecturer-authored free text (`§3` — "All evaluation and feedback are authored by human lecturers").
