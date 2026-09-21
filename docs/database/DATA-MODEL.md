# CaseTree AI — Data Model

**Status**: Scaffolded (see V1__init_schema.sql for the current migration)

---

## Core Tables

| Table | Description |
|---|---|
| `users` | All users: lecturers and students |
| `courses` | Lecturer courses |
| `teaching_materials` | Uploaded PDF/DOCX materials |
| `cases` | Decision tree case studies |
| `case_nodes` | Situation nodes in a decision tree |
| `case_options` | Decision options at each node |
| `simulation_sessions` | Student simulation sessions |
| `student_arguments` | Student written justifications at each node |
| `debate_sessions` | AI Debate Assistant sessions |
| `debate_messages` | Individual messages in a debate session |

## Vector/Embedding Tables (managed by FastAPI AI Service)

| Table | Description |
|---|---|
| `document_chunks` | Text chunks with pgvector embeddings |

## Key Constraints

- UUID primary keys throughout
- TIMESTAMPTZ for all timestamps
- `cases.status` CHECK constraint: DRAFT, REVIEWED, APPROVED, PUBLISHED
- `case_options.next_node_id` can be NULL (terminal path)
- Cycle detection is enforced at application layer (not DB constraint)
- `debate_sessions.current_round` max enforced at application layer (max=2)

## Migrations

All migrations managed by Flyway.
Migration files in `backend/src/main/resources/db/migration/`.
**Never modify existing migration files.** Create new V2__, V3__ files for changes.

## Naming Convention

- Table names: `snake_case`, plural
- Column names: `snake_case`
- Primary keys: `id UUID`
- Foreign keys: `<referenced_table_singular>_id UUID`
- Timestamps: `created_at TIMESTAMPTZ`, `updated_at TIMESTAMPTZ`
