# Security Policy — EduBranch AI

## Reporting a Vulnerability

If you discover a security vulnerability in EduBranch AI, **do not create a public GitHub issue**.

Please report it privately by emailing the project maintainer or opening a GitHub Security Advisory:
`Settings → Security → Advisories → New draft security advisory`

We will acknowledge your report within **72 hours** and aim to provide a fix timeline within **7 days** for critical issues.

---

## Security Scope

The following areas are in scope for security reporting:

- Authentication bypass or JWT vulnerabilities
- Authorization failures (e.g., student accessing unpublished cases)
- SQL injection, XSS, CSRF vulnerabilities
- File upload vulnerabilities (malicious file bypass)
- Exposure of internal service endpoints (FastAPI)
- Prompt injection through uploaded teaching materials
- Exposure of secrets or API keys in responses or logs
- Insecure direct object references (IDOR)
- Data leakage between lecturers/courses/students

---

## Security Architecture

### 1. Authentication

- The **Backend Gateway (NestJS)** handles all authentication via JWT (JSON Web Token)
- Passwords are hashed using BCrypt — plaintext passwords are never stored
- JWT tokens are validated on every protected request
- Refresh token rotation is implemented for extended sessions
- Failed login attempts are logged

### 2. Authorization

- Role-based access control: `LECTURER` and `STUDENT` roles
- The **Backend Gateway (NestJS)** enforces ownership: lecturers can only access their own courses and materials
- Students can only access published cases assigned to them
- **A student must never receive a case that is not in `PUBLISHED` status**
- Authorization is enforced server-side — never trust client-provided owner IDs

### 3. File Upload Security

- Only PDF and DOCX files are accepted (MIME type + extension validation)
- Maximum file size is enforced (configurable via `MAX_UPLOAD_SIZE_MB`)
- Files are stored in MinIO (object storage), never served as executable code
- File names are sanitized and stored under system-generated IDs

### 4. Internal Service Protection

- FastAPI AI Service is an **internal service** and must never be exposed to the public internet
- Communication between the **Backend Gateway (NestJS)** and the AI Service requires a shared internal API key (`X-Internal-API-Key` header)
- The AI Service must only listen on an internal Docker network interface in production

### 5. Prompt Injection Protection

- Uploaded teaching materials and retrieved RAG chunks are treated as **untrusted data**
- All retrieved content passed to the LLM MUST be enclosed in `<sources>...</sources>` boundary
- Retrieved content must never be able to override system instructions or prompt templates
- User-provided text (student arguments) must be validated and length-limited before being sent to the LLM

### 6. AI Governance — Critical Rules

> **The AI Debate Assistant MUST NOT:**
> - Assign academic grades
> - Make pass/fail academic decisions
> - Perform academic integrity judgments
> - Provide final evaluations of student performance
>
> The Debate Assistant is a **Devil's Advocate** tool: it generates targeted counter-questions only.
> All academic decisions remain with the lecturer.

### 7. Secret Management

- **Never** commit `.env` files or actual credentials to Git
- **Never** hardcode API keys, passwords, or connection strings in source code
- **Never** expose API keys, internal service URLs, or secrets in REST API responses
- **Never** log sensitive data (passwords, tokens, API keys)
- All secrets are managed via environment variables, loaded from `.env` files (excluded from Git)
- Enable the repository pre-commit safeguard via `git config core.hooksPath .githooks` to prevent accidental commits of `.env` and credentials
- Rotate credentials immediately if accidentally exposed

### 8. Data Privacy

- Student simulation data, arguments, and debate history are private to the student and the relevant lecturer
- No student data is shared across courses or lecturers without explicit authorization
- Research/evaluation data exports must be anonymized (see `docs/research/EVALUATION-DESIGN.md`)

### 9. CORS

- Allowed origins are explicitly configured via `CORS_ALLOWED_ORIGINS` environment variable
- In production, only the frontend domain is allowed
- FastAPI does not expose CORS to external origins

### 10. Database Security

- All database access goes through the Backend Gateway repository layer — no raw SQL string concatenation
- pgvector queries use parameterized queries
- Database credentials are externalized in environment variables
- Connection pool is bounded (min/max configurable)

---

## Supported Versions

| Version | Supported |
| :--- | :--- |
| `main` (latest) | ✅ |
| `develop` | ⚠️ Development branch — may contain known issues |
| Older releases | ❌ |
