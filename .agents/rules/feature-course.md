---
description: Rules for the Course domain in EduBranch AI.
trigger: keyword
keywords: [course, lecturer course, course management, course ownership]
---

# Feature Rules: Course & Lecturer Context

## Scope
Backend Gateway (NestJS `backend/`) — `course/` module.

## Included
- Lecturer creates/updates/deactivates courses
- Course owns: name, description, course code, lecturerId
- Course is the grouping context for teaching materials and cases
- Lecturer can only access their own courses (ownership enforcement)

## Excluded
- Student enrollment management — not in MVP scope
- Course marketplace or discovery — out of scope
- Multi-instructor ownership — single lecturer per course in MVP

## Service Owner
Backend Gateway (NestJS `backend/`)

## Constraints
- Always filter by `lecturerId = currentUser.id` when listing courses
- A course cannot be deleted if it has associated cases or materials (soft-delete only)
- `courseId` is a required foreign key for both TeachingMaterial and Case

## Testing Expectations
- Lecturer can only see their own courses
- Another lecturer cannot access another's courses (403)
