---
description: Rules for lecturer statistics in Edu-Branch-AI.
trigger: keyword
keywords: [statistics, analytics, branch selection, participation, completion]
---

# Feature Rules: Lecturer Statistics

## Scope
Backend Gateway (NestJS `backend/`) — `statistics/` module.
Frontend — `features/statistics/`.

## Included
- Branch selection frequency per node per case
- Participation count per case (how many students started/completed)
- Completion rate per case
- Simple reasoning inspection (list of student reasoning for a case)

## Excluded
- Complex learning analytics dashboard — out of scope
- Student ranking or grading — out of scope
- Cohort analysis — out of scope
- Export to LMS — out of scope

## Service Owner
Backend Gateway (NestJS backend, read-only aggregation queries)

## Constraints
- Statistics are read-only — no mutation
- Accessible only by the course''s lecturer
- Keep queries simple — this is NOT a large analytics platform
- Do not expose personally identifiable student data in aggregate statistics without consent

## Testing Expectations
- Test that non-owners cannot access statistics for a course
