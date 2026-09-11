---
description: Rules for student argument capture in EduBranch AI.
trigger: keyword
keywords: [argument, justification, student argument, reasoning, written response]
---

# Feature Rules: Student Argument Capture

## Scope
Backend Gateway (NestJS `backend/`) — `argument/` module.
Frontend — `features/arguments/`.

## Included
- After selecting an option, student submits a written justification/argument
- Argument is persisted linked to: session + case + node + option
- Argument is the trigger for the AI Debate Assistant
- Student may view their submitted arguments for a session

## Excluded
- AI grading of arguments — Debate Assistant only asks counter-questions
- Automated pass/fail based on argument quality — out of scope
- Plagiarism detection — out of scope

## Service Owner
Backend Gateway (NestJS `backend/`)

## Constraints
- Argument text should have a minimum length (10 chars) and maximum length (2000 chars)
- Argument is stored as plain text (no HTML, sanitize on input)
- StudentId is always from JWT — never trust client-provided studentId
- One argument per (session, node, option) combination

## Testing Expectations
- Test argument length validation
- Test that a student cannot submit arguments for another student''s session
