---
description: Rules for Lecturer Feedback / Open Review in CaseTree AI.
trigger: keyword
keywords: [lecturer feedback, open review, lecturer review, feedback, commentary]
---

# Feature Rules: Lecturer Feedback & Review

## Scope
Backend Gateway (NestJS `backend/`) — `lecturer-feedback/` module.
Frontend — `pages/lecturer/LecturerFeedbackPage.tsx`.

## Included
- Lecturer inspects student work across both learning modes:
  - Branching Study: student attempt path, terminal outcome, and submitted reasoning
  - Review Study: student proposed solution, reasoning, and optional analysis
- Lecturer authors qualitative feedback (`feedback_text`)
- Persisted to `lecturer_feedback` table:
  - Supports exactly one target: `branching_attempt_id` XOR `review_submission_id` (`chk_feedback_one_target`)
  - `lecturer_id` set from JWT
- Submitting feedback on Review Study advances `review_study_submissions.submission_status` from `SUBMITTED` to `REVIEWED`
- Student can view lecturer feedback on their attempt/submission

## Excluded
- AI-generated grading or automatic score calculation
- Automatic pass/fail determinations
- LMS gradebook synchronization in MVP

## Service Owner
Backend Gateway: feedback persistence, role authorization (LECTURER only), lifecycle state transitions.
Frontend: Lecturer Feedback dashboard & editor UI.

## Constraints
- Only authenticated users with role `LECTURER` can create or edit feedback
- Lecturer must be the owner of the course to which the case belongs
- `feedback_text` is required (NOT NULL) and sanitized
- One target per feedback row enforced at database level (`chk_feedback_one_target`)
