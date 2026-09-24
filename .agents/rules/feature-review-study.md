---
description: Rules for the Review Study learning mode in CaseTree AI.
trigger: keyword
keywords: [review study, case analysis, proposed solution, review submission]
---

# Feature Rules: Review Study Learning Mode

## Scope
Backend Gateway (NestJS `backend/`) — `review-study/` module.
Frontend — `pages/student/ReviewStudyPage.tsx` and `pages/student/ReviewFeedbackPage.tsx`.

## Included
- Student accesses a `PUBLISHED` case with `learning_mode = 'REVIEW_STUDY'`
- Case presents `context_text` (case context/data) and `problem_text` (problem/question to analyze)
- Student submits their proposed solution and reasoning:
  - `student_analysis` (optional/nullable TEXT — R2 Confirmed Option A)
  - `proposed_solution` (NOT NULL TEXT)
  - `reasoning_text` (NOT NULL TEXT)
- Exactly one submission per student per Review Study case (`UNIQUE(student_id, case_id)`)
- System accepts several reasonable solutions and reasoning — does NOT determine a single correct answer
- Submission triggers optional AI Reasoning / Challenge Support (target: `review_submission_id`)
- Lecturer reviews submission and provides feedback (`lecturer_feedback`)
- Forward-only submission lifecycle: `SUBMITTED` → `REVIEWED` (after lecturer feedback) → `REFLECTED` (after student reflection)

## Excluded
- Decision tree navigation or branching nodes (Review Study does not use `case_nodes` / `case_options`)
- Automated grading or scoring of solutions/reasoning
- Automatic correctness determination
- Multi-student collaborative editing

## Service Owner
Backend Gateway: submission persistence, uniqueness enforcement, lifecycle transitions.
Frontend: Review Study workspace UI (context viewer, solution/reasoning forms, feedback/reflection viewer).

## Constraints
- Case must have `status = 'PUBLISHED'` and `learning_mode = 'REVIEW_STUDY'`
- `student_id` is always derived from JWT
- `proposed_solution` and `reasoning_text` must meet minimum length validation (min 10 chars)
- AI never grades or decides correctness
