# Changelog — Edu-Branch-AI

All notable changes to Edu-Branch-AI are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Changed
- **Product reorientation**: CaseTree-AI → Edu-Branch-AI. Product name, positioning, and all user-facing references updated across README, docs, UI, and source comments.
- **Branching Study flow corrected**: Experience phase is now seamless (no reasoning form or consequence card between Decision Points). REVIEW phase (post-journey retrospective) introduced as the primary site for reasoning capture and path analysis. See `docs/features/FEATURE-BRANCHING-STUDY.md`.
- **AI positioning corrected**: AI Reasoning / Challenge Support replaces "Debate Assistant / Devil's Advocate" in all documentation and source files.
- **Product positioning corrected**: Edu-Branch-AI is positioned as a case-based learning platform, not a "Branching Decision Tree Simulator".

---

## [0.0.1] - 2026-09-11

### Scaffolded
- Initial repository skeleton for Edu-Branch-AI (formerly CaseTree-AI)
- NestJS 10 backend project structure with domain modules: `auth`, `user`, `course`, `material`, `case`, `branching-attempt`, `reasoning`, `challenge-support`, `review-study`, `lecturer-feedback`, `statistics`, `evaluation`, `notification`, `common`
- FastAPI AI service project structure with domain packages: `core`, `providers`, `ingestion`, `retrieval`, `generation`, `challenge_support`, `evaluation`
- React 19 + Vite + TypeScript + TailwindCSS v4 frontend with feature-based module structure
- PostgreSQL 16 + pgvector + Redis 7 + MinIO Docker Compose infrastructure
- GitHub Actions CI/CD workflows for backend, ai-service, and frontend
- Agent/AI coding rules in `.agents/rules/`
- Architecture documentation in `docs/architecture/`
- AI documentation in `docs/ai/`
- Database documentation in `docs/database/`
- Research/evaluation documentation in `docs/research/`
- QA and testing strategy in `docs/qa/`
- `.env.example` for all services
- CONTRIBUTING.md, SECURITY.md, CODE_OF_CONDUCT.md

### Added
- Repository initialized
- Proposal document preserved in `docs/`
