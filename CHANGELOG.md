# Changelog — CaseTree AI

All notable changes to CaseTree AI are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Scaffolded
- Initial repository skeleton for CaseTree AI
- Spring Boot 3 backend project structure with domain packages: `auth`, `user`, `course`, `material`, `case`, `simulation`, `argument`, `debate`, `statistics`, `evaluation`, `notification`, `common`
- FastAPI AI service project structure with domain packages: `core`, `providers`, `ingestion`, `retrieval`, `generation`, `debate`, `evaluation`
- React + Vite + TypeScript + TailwindCSS frontend with feature-based module structure
- PostgreSQL + pgvector + Redis + MinIO Docker Compose infrastructure
- GitHub Actions CI/CD workflows for backend, ai-service, and frontend
- Agent/AI coding rules in `.agents/rules/`
- Architecture documentation in `docs/architecture/`
- AI documentation in `docs/ai/`
- Database documentation in `docs/database/`
- Frontend documentation in `docs/frontend/`
- Research/evaluation documentation in `docs/research/`
- QA and testing strategy in `docs/qa/`
- `.env.example` for all services
- CONTRIBUTING.md, SECURITY.md, CODE_OF_CONDUCT.md

---

## [0.0.1] - 2026-09-11

### Added
- Repository initialized
- Proposal document preserved in `docs/`
