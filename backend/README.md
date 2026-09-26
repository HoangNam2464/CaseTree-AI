# Edu-Branch-AI — Backend Gateway

Node.js (NestJS + TypeScript) REST API Gateway for the Edu-Branch-AI platform.

## Responsibilities

- Authentication & JWT issuance (Lecturer / Student roles)
- User and role management
- Course and teaching material metadata
- Case lifecycle state machine (`DRAFT → REVIEWED → APPROVED → PUBLISHED`)
- Student simulation session persistence
- Student argument capture at decision nodes
- Debate session history persistence & 2-round cap enforcement
- Lecturer statistics aggregations
- Research evaluation boundary
- REST API gateway for the React frontend
- Internal HTTP client to call internal FastAPI AI Service

## Technology

- **Runtime**: Node.js 20+
- **Language**: TypeScript (strict mode)
- **Framework**: NestJS 10
- **Database**: PostgreSQL 16 + pgvector (`pg` / TypeORM)
- **Migrations**: SQL Schema (`backend/migrations/V1__init_schema.sql`)
- **Cache**: Redis 7
- **Object Storage**: MinIO S3 SDK
- **Validation**: `class-validator`, `class-transformer`
- **Internal HTTP Client**: Axios / `@nestjs/axios` for FastAPI AI Service calls

## Module Structure (by domain/feature)

```
backend/src/
├── app.module.ts            ← Root application module
├── main.ts                  ← Application entry point (Port 8080, /api/v1)
├── common/
│   ├── health/              ← Health check controller (/api/v1/health)
│   ├── filters/             ← Global exception filters
│   └── interceptors/        ← Response transformation interceptors
├── migrations/
│   └── V1__init_schema.sql  ← Initial PostgreSQL + pgvector schema
└── modules/
    ├── auth/                ← Authentication, JWT, login, registration
    ├── user/                ← User entity, role management
    ├── course/              ← Course ownership and management
    ├── material/            ← Teaching material upload and metadata
    ├── case/                ← Case lifecycle, decision tree domain model
    ├── simulation/          ← Student simulation sessions
    ├── argument/            ← Student arguments at decision nodes
    ├── debate/              ← Debate session history persistence
    ├── statistics/          ← Lecturer statistics queries
    ├── notification/        ← Notification extension point
    └── evaluation/          ← Research/evaluation data boundary
```

## Local Setup

```bash
# 1. Start infrastructure (from project root)
docker compose up -d

# 2. Configure environment
cp .env.example .env

# 3. Install dependencies
npm install

# 4. Start in development mode
npm run start:dev
# Backend Gateway runs at http://localhost:8080/api/v1
```

## Build & Test

```bash
npm run build
npm run test
```
