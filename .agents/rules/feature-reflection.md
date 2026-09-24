---
description: Rules for Student Reflection in CaseTree AI.
trigger: keyword
keywords: [reflection, student reflection, post-outcome, reflection text, reflect]
---

# Feature Rules: Student Reflection

## Scope
Backend Gateway (NestJS `backend/`) — tracked on `branching-attempt/` and `review-study/` modules.
Frontend — `pages/student/ReflectionPage.tsx` and `pages/student/ReviewFeedbackPage.tsx`.

## Included
- Student writes reflective commentary after completing an activity:
  - Branching Study: after reaching a terminal outcome node (`outcome_node_id` NOT NULL, `is_completed = TRUE`), student reflects on decisions made and consequences encountered (`branching_attempts.reflection_text`)
  - Review Study: after receiving lecturer feedback (`submission_status = 'REVIEWED'`), student reflects on feedback and compares their thinking (`review_study_submissions.reflection_text`)
- Status tracking:
  - `reflection_status`: 'NOT_STARTED' | 'SUBMITTED'
  - `reflection_submitted_at`: timestamp recorded upon submission
- Forward-only state transition: once submitted, `reflection_status` becomes `SUBMITTED`
- Completing reflection in Review Study transitions `submission_status` from `REVIEWED` to `REFLECTED`

## Excluded
- AI grading of student reflection
- Comparison engine / automatic rating of reflection depth
- Obligatory word count scoring

## Service Owner
Backend Gateway: persistence on `branching_attempts` and `review_study_submissions`.
Frontend: Reflection submission screens and history viewer.

## Constraints
- In Branching Study, reflection is allowed only when `is_completed = TRUE`
- In Review Study, reflection is allowed only after lecturer feedback is present (`submission_status = 'REVIEWED'`)
- Student ID must match the owning attempt / submission
- Once `reflection_status = 'SUBMITTED'`, text is immutable in that attempt
