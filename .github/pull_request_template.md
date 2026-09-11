## Description

<!-- What does this PR do? What problem does it solve? -->

## Type of Change

- [ ] `feat` — New feature
- [ ] `fix` — Bug fix
- [ ] `refactor` — Code restructuring (no logic change)
- [ ] `docs` — Documentation update
- [ ] `test` — Adding or fixing tests
- [ ] `chore` — Dependency updates, config changes
- [ ] `ci` — CI/CD workflow changes

## Scope

- [ ] `backend` (Spring Boot)
- [ ] `ai-service` (FastAPI)
- [ ] `frontend` (React)
- [ ] `infra` (Docker, compose, scripts)
- [ ] `docs` (Documentation)

## Checklist

### Architecture Compliance
- [ ] Frontend does NOT call FastAPI directly
- [ ] FastAPI is NOT exposed to the internet
- [ ] Retrieved document chunks are wrapped in `<sources>...</sources>` (if AI changes)
- [ ] Case publication gate is maintained (students only access PUBLISHED cases)
- [ ] AI Debate Assistant does NOT grade or pass/fail students (if debate changes)

### Code Quality
- [ ] Branch created from `develop` (not `main`)
- [ ] Branch name follows naming convention: `feature/`, `fix/`, `refactor/`, etc.
- [ ] All commits follow the format: `type(scope): description`
- [ ] No secrets, API keys, or `.env` files committed
- [ ] Code is formatted and linted
- [ ] No `console.log` / `System.out.println` left in production code

### Testing
- [ ] Backend: `./mvnw test` passes
- [ ] AI Service: `pytest` passes
- [ ] Frontend: `npm run build` succeeds
- [ ] CI workflows are green

### Documentation
- [ ] Swagger/API docs updated if endpoints changed
- [ ] Feature rules in `.agents/rules/` updated if architecture changed
- [ ] Flyway migration added if schema changed (do not modify existing migrations)

## Related Issues

<!-- Link to issue(s) this PR addresses: Closes #XXX -->

## Screenshots / Evidence

<!-- For UI changes, attach before/after screenshots -->
<!-- For API changes, attach request/response examples -->
