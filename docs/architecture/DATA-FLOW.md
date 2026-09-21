# CaseTree AI — System Data Flows & Sequences

> **Document Status**: Authoritative Architecture Specification  
> **Purpose**: Traces end-to-end data flows and lifecycle sequences across the system components.

---

## 1. Flow 1: Teaching Material Upload & Document Processing

```mermaid
sequenceDiagram
    autonumber
    actor Lecturer
    participant FE as React Frontend
    participant BE as Backend Gateway
    participant S3 as MinIO (Object Storage)
    participant AI as FastAPI AI Service
    participant DB as PostgreSQL + pgvector

    Lecturer->>FE: Uploads PDF / DOCX file
    FE->>BE: POST /api/v1/courses/{courseId}/materials (Multipart Form)
    BE->>BE: Validate file extension & MIME type
    BE->>S3: PutObject(bucket="casetree-materials", key=file_uuid)
    BE->>DB: INSERT INTO teaching_materials (status='PENDING')
    BE->>AI: POST /internal/v1/ingestion/process (material_id, s3_key, course_id)
    AI->>S3: GetObject(key=file_uuid)
    AI->>AI: Parse text (PyPDF / python-docx)
    AI->>AI: Split into chunks (RecursiveCharacterTextSplitter)
    AI->>AI: Generate embeddings (text-embedding-004 / text-embedding-3-small)
    AI->>DB: INSERT INTO document_chunks (chunk_text, embedding, metadata)
    AI-->>BE: 200 OK (chunk_count=N, status='COMPLETED')
    BE->>DB: UPDATE teaching_materials SET processing_status='COMPLETED', chunk_count=N
    BE-->>FE: 200 OK (Material processed successfully)
```

---

## 2. Flow 2: AI Case Generation (RAG + Structured JSON Output)

```mermaid
sequenceDiagram
    autonumber
    actor Lecturer
    participant FE as React Frontend
    participant BE as Backend Gateway
    participant AI as FastAPI AI Service
    participant DB as PostgreSQL + pgvector
    participant LLM as LLM Provider (Gemini / OpenAI)

    Lecturer->>FE: Clicks "Generate Case Study" (provides topic hint, material selection)
    FE->>BE: POST /api/v1/cases/generate (courseId, materialIds, topic)
    BE->>AI: POST /internal/v1/generation/generate-case (course_id, material_ids, topic)
    AI->>AI: Generate query embedding for topic
    AI->>DB: Cosine similarity query over document_chunks (WHERE course_id=... ORDER BY embedding <=> query LIMIT 5)
    DB-->>AI: Top-K context chunks
    AI->>AI: Format prompt: System Persona + <sources>[chunks]</sources> + User Prompt
    AI->>LLM: generate_content(prompt, response_schema=DecisionTreeOutput)
    LLM-->>AI: Structured JSON decision tree
    AI->>AI: Validate JSON schema & BFS cycle detection (no loops, no orphans, terminal exists)
    AI-->>BE: 200 OK (Validated DecisionTree JSON)
    BE->>DB: INSERT INTO cases (status='DRAFT', title, ...)
    BE->>DB: INSERT INTO case_nodes & case_options
    BE-->>FE: 201 Created (Case generated in DRAFT status)
    FE->>Lecturer: Renders decision tree in form editor
```

---

## 3. Flow 3: Lecturer Review, Edit & Publishing Workflow

```mermaid
sequenceDiagram
    autonumber
    actor Lecturer
    participant FE as React Frontend (ReactFlow)
    participant BE as Backend Gateway
    participant DB as PostgreSQL

    Lecturer->>FE: Views decision tree in ReactFlow editor
    Lecturer->>FE: Modifies situation text, options, or consequences
    FE->>BE: PUT /api/v1/cases/{caseId} (updated nodes & options)
    BE->>BE: Validate tree integrity (no cycles, reachability from root)
    BE->>DB: UPDATE case_nodes, case_options, cases (status='REVIEWED')
    BE-->>FE: 200 OK (Updated)
    Lecturer->>FE: Clicks "Approve Case"
    FE->>BE: POST /api/v1/cases/{caseId}/approve
    BE->>DB: UPDATE cases SET status='APPROVED'
    BE-->>FE: 200 OK
    Lecturer->>FE: Clicks "Publish to Students"
    FE->>BE: POST /api/v1/cases/{caseId}/publish
    BE->>DB: UPDATE cases SET status='PUBLISHED'
    BE-->>FE: 200 OK (Case now accessible to students)
```

---

## 4. Flow 4: Student Simulator & Decision Argument Capture

```mermaid
sequenceDiagram
    autonumber
    actor Student
    participant FE as React Frontend (Simulator)
    participant BE as Backend Gateway
    participant DB as PostgreSQL

    Student->>FE: Enters Simulator for published case
    FE->>BE: POST /api/v1/cases/{caseId}/simulation/start
    BE->>DB: Verify case status is PUBLISHED
    BE->>DB: INSERT INTO simulation_sessions (student_id, current_node=root_node_id)
    BE-->>FE: 200 OK (root CaseNode: situation, options)
    Student->>FE: Selects Option B, reads immediate consequence
    Student->>FE: Types short justification argument
    FE->>BE: POST /api/v1/simulation/{sessionId}/decision (nodeId, optionId, argumentText)
    BE->>DB: INSERT INTO student_arguments (argument_text, option_id, node_id)
    BE->>DB: UPDATE simulation_sessions SET current_node_id=option.next_node_id
    BE-->>FE: 200 OK (Saved; triggers Debate Assistant modal)
```

---

## 5. Flow 5: AI Debate Assistant (Devil's Advocate Challenge)

```mermaid
sequenceDiagram
    autonumber
    actor Student
    participant FE as React Frontend
    participant BE as Backend Gateway
    participant AI as FastAPI AI Service
    participant LLM as LLM Provider (Gemini / OpenAI)
    participant DB as PostgreSQL

    FE->>BE: POST /api/v1/debate/start (argumentId)
    BE->>DB: INSERT INTO debate_sessions (argument_id, current_round=1)
    BE->>AI: POST /internal/v1/debate/challenge (argument_text, situation, option, round=1)
    AI->>AI: System Prompt: "You are a Socratic Devil's Advocate. Ask 1 counter-question. DO NOT GRADE."
    AI->>LLM: Generate counter-question
    LLM-->>AI: Single targeted counter-question
    AI-->>BE: 200 OK (question_text)
    BE->>DB: INSERT INTO debate_messages (role='AI_ASSISTANT', round=1, content=question_text)
    BE-->>FE: 200 OK (Displays Round 1 counter-question to Student)
    
    opt Student Responds (Round 2)
        Student->>FE: Types rebuttal / response
        FE->>BE: POST /api/v1/debate/{debateId}/respond (response_text)
        BE->>DB: INSERT INTO debate_messages (role='STUDENT', round=2, content=response_text)
        BE->>AI: POST /internal/v1/debate/challenge (student_response, round=2)
        AI->>LLM: Generate final counter-question / reflection
        LLM-->>AI: Final reflection question
        AI-->>BE: 200 OK (final_question)
        BE->>DB: INSERT INTO debate_messages (role='AI_ASSISTANT', round=2, content=final_question)
        BE->>DB: UPDATE debate_sessions SET current_round=2, is_completed=TRUE
        BE-->>FE: 200 OK (Debate completed — no further rounds permitted)
    end
```

---

## 6. Flow 6: Lecturer Statistics & Research Data Inspection

```mermaid
sequenceDiagram
    autonumber
    actor Lecturer
    participant FE as React Frontend (Statistics)
    participant BE as Backend Gateway
    participant DB as PostgreSQL

    Lecturer->>FE: Navigates to Course Statistics
    FE->>BE: GET /api/v1/courses/{courseId}/statistics
    BE->>DB: Aggregate branch selections (COUNT per case_option_id)
    BE->>DB: Aggregate session completion rates
    BE-->>FE: 200 OK (JSON with branch distribution, student argument list)
    FE->>Lecturer: Renders decision breakdown charts & argument review table
```
