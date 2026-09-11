---
description: Rules for authentication and authorization implementation in EduBranch AI.
trigger: keyword
keywords: [auth, login, register, jwt, security, role, permission, password]
---

# Feature Rules: Authentication & Role Management

## Scope
Backend Gateway (NestJS `backend/`) — `auth/` and `user/` modules.

## Included
- User registration (email, password, fullName, role selection: LECTURER | STUDENT)
- Login with email/password → returns JWT access + refresh tokens
- JWT access token validation on protected endpoints
- Refresh token rotation
- Role-based access control (RBAC): LECTURER and STUDENT roles
- Password hashing using BCrypt (never store plaintext)
- JWT authentication guard and strategy

## Excluded
- Social login (Google, Facebook) — out of scope
- OAuth2 — out of scope
- Multi-factor authentication — out of scope
- Admin/system operator role — not in MVP

## Service Owner
Backend Gateway (NestJS `backend/`)

## Constraints
- Passwords MUST be hashed with BCrypt before storage
- JWT secret loaded from environment variable JWT_SECRET — never hardcoded
- Failed login attempts should be logged (without exposing user data)
- Never expose passwordHash or internal user IDs in API responses
- Authorization is enforced server-side — never trust client-provided user ID
- Lecturer can only access their own courses/materials/cases
- Student can only access PUBLISHED cases

## Testing Expectations
- Unit tests for JWT generation/validation
- Integration test for login → token validation flow
- Test that student cannot access lecturer-only endpoints
- Test that unauthorized user receives 401
