---
description: Rules for the notification extension point in CaseTree AI.
trigger: keyword
keywords: [notification, email, reminder, deadline, assignment]
---

# Feature Rules: Notification Extension Point

## Scope
Backend Gateway (NestJS `backend/`) — `notification/` module.

## Included (Scaffolded only)
- Notification entity (recipient, type, message, read status)
- Extension point for: assignment reminder, deadline reminder, in-app notification

## Excluded
- Email delivery implementation — not in MVP
- Push notifications — out of scope
- Complex notification preferences — out of scope
- Real-time WebSocket notifications — out of scope

## Service Owner
Backend Gateway (NestJS backend)

## Constraints
- Keep this intentionally minimal in the bootstrap phase
- Do NOT build a complex notification platform
