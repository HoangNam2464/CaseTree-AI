# Feature: Account, Authentication & Roles

> **Authoritative Traceability**: Items 1, 2, 3 (Proposal Section 2 p. 6, Section 4 p. 7, Section 6 p. 10)  
> **Target Package / Module**: Backend `auth/`, `user/` · Frontend `features/auth/`

---

## 1. Purpose
Provides secure identity management, authentication, and role-based access control (RBAC) separating university **Lecturers** and **Students**. Ensures that case authoring, review, and publishing workflows are restricted to lecturers, while case simulation and argument submission are scoped to enrolled students.

---

## 2. Actors
- **Lecturer**: Authenticated university instructor who manages courses, uploads materials, and reviews/publishes cases.
- **Student**: Authenticated university learner who accesses published cases, role-plays decision trees, and debates with the AI assistant.
- **System**: Backend security filter validating JWT tokens and enforcing ownership boundaries.

---

## 3. Scope
- User registration and login via email and password.
- Secure password hashing using BCrypt.
- Stateless session management using JSON Web Tokens (JWT).
- Role segregation (`LECTURER`, `STUDENT`).
- Protected API routes and client-side route guarding.

---

## 4. Functional Requirements
- **FR-AUTH-01**: The system shall allow users to register with email, password, full name, and role (`LECTURER` or `STUDENT`).
- **FR-AUTH-02**: The system shall authenticate users against stored password hashes and issue signed JWT access tokens.
- **FR-AUTH-03**: The system shall enforce role checks on all protected API endpoints:
  - Lecturer-only endpoints: Course creation, material upload, case generation, case review/edit, approval, publication, statistics.
  - Student-only endpoints: Simulation session start, decision option selection, argument submission, debate participation.
- **FR-AUTH-04**: The system shall provide an endpoint to inspect the currently authenticated user profile and active role (`GET /api/v1/auth/me`).

---

## 5. Main Flow
1. User navigates to `/login` or `/register` in the React frontend.
2. User enters credentials (email, password).
3. Frontend sends `POST /api/v1/auth/login` to the Backend Gateway.
4. Backend verifies credentials against `users` table via BCrypt hash comparison.
5. Backend issues a JWT access token containing `userId`, `email`, and `role`.
6. Frontend stores the token in memory / Zustand store and configures the Axios Bearer interceptor.
7. User is routed to `/lecturer/courses` (if Lecturer) or `/student` dashboard (if Student).

---

## 6. Inputs
- `email`: Valid university/standard email string (required, unique).
- `password`: String with minimum security constraints (required).
- `fullName`: Human-readable name string (required for registration).
- `role`: Enum string (`LECTURER` or `STUDENT`).

---

## 7. Outputs
- Success: HTTP 200/201 with `{ success: true, data: { token, user: { id, email, fullName, role } } }`.
- Failure: HTTP 401 Unauthorized or 400 Bad Request with standardized error message.

---

## 8. Business Rules
- **BR-AUTH-01**: A user may possess only one active system role (`LECTURER` or `STUDENT`) per account.
- **BR-AUTH-02**: Plaintext passwords must never be logged or stored in the database.
- **BR-AUTH-03**: Students must never be authorized to invoke case generation, review, or publication endpoints.
- **BR-AUTH-04**: Expired or tampered JWTs must be immediately rejected with HTTP 401.

---

## 9. Permissions
- Public: `POST /api/v1/auth/login`, `POST /api/v1/auth/register`, `GET /api/v1/health`.
- Authenticated (Any Role): `GET /api/v1/auth/me`.
- Role `LECTURER`: All `/api/v1/courses/**`, `/api/v1/cases/**`, `/api/v1/materials/**`.
- Role `STUDENT`: All `/api/v1/simulation/**`, `/api/v1/debate/**`.

---

## 10. Dependencies
- Relational Database table `users`.
- Backend cryptographic libraries (BCrypt, JJWT / standard JWT parser).
- Frontend Axios interceptor (`src/services/apiClient.ts`).

---

## 11. Data Involved
- **Table `users`**:
  - `id`: UUID (Primary Key)
  - `email`: VARCHAR(255) UNIQUE NOT NULL
  - `password_hash`: VARCHAR(255) NOT NULL
  - `full_name`: VARCHAR(255) NOT NULL
  - `role`: VARCHAR(50) NOT NULL (`LECTURER` | `STUDENT`)
  - `is_active`: BOOLEAN DEFAULT TRUE
  - `created_at`, `updated_at`: TIMESTAMPTZ

---

## 12. Error / Edge Cases
- Invalid credentials: Return HTTP 401 with generic "Invalid email or password" to prevent user enumeration.
- Duplicate email registration: Return HTTP 409 Conflict.
- Malformed JWT header: Return HTTP 401 Unauthorized.
- User inactive (`is_active = false`): Block login with HTTP 403 Forbidden.

---

## 13. Out of Scope
- Social OAuth / OpenID login (Google, Facebook, GitHub) — strictly excluded.
- Single Sign-On (SSO) with university campus LDAP/SAML.
- Multi-factor authentication (MFA / SMS OTP).
- Multi-tenant university administration dashboards.

---

## 14. Related Documentation
- [`docs/requirements/REQUIREMENT-TRACEABILITY.md`](../requirements/REQUIREMENT-TRACEABILITY.md) (Items 1, 2, 3)
- [`docs/architecture/SERVICE-BOUNDARIES.md`](../architecture/SERVICE-BOUNDARIES.md)
- [`docs/database/DATA-MODEL.md`](../database/DATA-MODEL.md)

---

## 15. Implementation Status
**Structurally Scaffolded**  
*(Domain entities/types `User`, `Role` in `backend/src/modules/user/`, database table `users`, and frontend layout shells exist; production authentication workflows and controllers remain unimplemented.)*
