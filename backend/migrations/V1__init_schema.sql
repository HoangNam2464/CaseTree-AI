-- ==============================================================================
-- EduBranch AI — Initial Schema Migration V1
-- ==============================================================================
-- Establishes the base schema for all core domain entities.
-- Uses UUID as primary key strategy throughout.
-- All timestamps use TIMESTAMPTZ (timezone-aware).
-- ==============================================================================

-- Enable pgvector extension (required for embedding columns in ai-service tables)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS vector;

-- ==============================================================================
-- users
-- ==============================================================================
CREATE TABLE users (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email           VARCHAR(255) NOT NULL UNIQUE,
    password_hash   VARCHAR(255) NOT NULL,
    full_name       VARCHAR(255) NOT NULL,
    role            VARCHAR(50)  NOT NULL CHECK (role IN ('LECTURER', 'STUDENT')),
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ==============================================================================
-- courses
-- ==============================================================================
CREATE TABLE courses (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name            VARCHAR(255) NOT NULL,
    description     TEXT,
    course_code     VARCHAR(100),
    lecturer_id     UUID NOT NULL REFERENCES users(id),
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ==============================================================================
-- teaching_materials
-- ==============================================================================
CREATE TABLE teaching_materials (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    original_filename   VARCHAR(500) NOT NULL,
    stored_object_key   VARCHAR(1000) NOT NULL,
    mime_type           VARCHAR(100) NOT NULL,
    size_bytes          BIGINT,
    course_id           UUID NOT NULL REFERENCES courses(id),
    uploaded_by         UUID NOT NULL REFERENCES users(id),
    processing_status   VARCHAR(50) NOT NULL DEFAULT 'PENDING'
                            CHECK (processing_status IN ('PENDING', 'PROCESSING', 'COMPLETED', 'FAILED')),
    chunk_count         INTEGER,
    processing_error    TEXT,
    uploaded_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ==============================================================================
-- cases
-- ==============================================================================
CREATE TABLE cases (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title           VARCHAR(500) NOT NULL,
    description     TEXT,
    course_id       UUID NOT NULL REFERENCES courses(id),
    created_by      UUID NOT NULL REFERENCES users(id),
    status          VARCHAR(50) NOT NULL DEFAULT 'DRAFT'
                        CHECK (status IN ('DRAFT', 'REVIEWED', 'APPROVED', 'PUBLISHED')),
    version         INTEGER NOT NULL DEFAULT 1,
    root_node_id    UUID,  -- FK set after nodes are created
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ==============================================================================
-- case_nodes (Decision Tree nodes / situations)
-- ==============================================================================
CREATE TABLE case_nodes (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id         UUID NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
    situation       TEXT NOT NULL,
    is_terminal     BOOLEAN NOT NULL DEFAULT FALSE,
    node_index      INTEGER
);

-- ==============================================================================
-- case_options (Decision choices at each node)
-- ==============================================================================
CREATE TABLE case_options (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    node_id         UUID NOT NULL REFERENCES case_nodes(id) ON DELETE CASCADE,
    option_text     TEXT NOT NULL,
    consequence     TEXT NOT NULL,
    next_node_id    UUID REFERENCES case_nodes(id)
    -- NOTE: next_node_id=NULL means this option leads to a terminal state
    -- Cycle detection is enforced at the application service layer
);

-- Add FK from cases.root_node_id → case_nodes.id (deferred to allow circular reference)
ALTER TABLE cases ADD CONSTRAINT fk_cases_root_node
    FOREIGN KEY (root_node_id) REFERENCES case_nodes(id) DEFERRABLE INITIALLY DEFERRED;

-- ==============================================================================
-- simulation_sessions
-- ==============================================================================
CREATE TABLE simulation_sessions (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id      UUID NOT NULL REFERENCES users(id),
    case_id         UUID NOT NULL REFERENCES cases(id),
    current_node_id UUID REFERENCES case_nodes(id),
    is_completed    BOOLEAN NOT NULL DEFAULT FALSE,
    started_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at    TIMESTAMPTZ
);

-- ==============================================================================
-- student_arguments
-- ==============================================================================
CREATE TABLE student_arguments (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id      UUID NOT NULL REFERENCES simulation_sessions(id),
    student_id      UUID NOT NULL REFERENCES users(id),
    case_id         UUID NOT NULL REFERENCES cases(id),
    node_id         UUID NOT NULL REFERENCES case_nodes(id),
    option_id       UUID NOT NULL REFERENCES case_options(id),
    argument_text   TEXT NOT NULL,
    submitted_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ==============================================================================
-- debate_sessions
-- ==============================================================================
CREATE TABLE debate_sessions (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    argument_id     UUID NOT NULL UNIQUE REFERENCES student_arguments(id),
    current_round   INTEGER NOT NULL DEFAULT 0,
    is_completed    BOOLEAN NOT NULL DEFAULT FALSE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ==============================================================================
-- debate_messages
-- ==============================================================================
CREATE TABLE debate_messages (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id      UUID NOT NULL REFERENCES debate_sessions(id) ON DELETE CASCADE,
    round_number    INTEGER NOT NULL,
    role            VARCHAR(50) NOT NULL CHECK (role IN ('AI_ASSISTANT', 'STUDENT')),
    content         TEXT NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ==============================================================================
-- Indexes
-- ==============================================================================
CREATE INDEX idx_courses_lecturer_id      ON courses(lecturer_id);
CREATE INDEX idx_materials_course_id      ON teaching_materials(course_id);
CREATE INDEX idx_cases_course_id          ON cases(course_id);
CREATE INDEX idx_cases_status             ON cases(status);
CREATE INDEX idx_case_nodes_case_id       ON case_nodes(case_id);
CREATE INDEX idx_case_options_node_id     ON case_options(node_id);
CREATE INDEX idx_sessions_student_id      ON simulation_sessions(student_id);
CREATE INDEX idx_sessions_case_id         ON simulation_sessions(case_id);
CREATE INDEX idx_arguments_session_id     ON student_arguments(session_id);
CREATE INDEX idx_debate_sessions_arg_id   ON debate_sessions(argument_id);
CREATE INDEX idx_debate_messages_sess_id  ON debate_messages(session_id);
