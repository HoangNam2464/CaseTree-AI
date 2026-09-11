# Feature: Document Processing & RAG Retrieval

> **Authoritative Traceability**: Items 7, 8 (Proposal Section 4 p. 7, Section 6 p. 10, Section 7 p. 11)  
> **Target Package / Module**: AI Service `ingestion/`, `retrieval/` · Database `document_chunks` (pgvector)

---

## 1. Purpose
Extracts, chunks, embeds, and indexes university teaching materials to power Retrieval-Augmented Generation (RAG). Allows the AI Case Generator and AI Debate Assistant to retrieve semantically grounded course concepts, ensuring generated case studies and counter-questions align with authentic course syllabi and lecture content.

---

## 2. Actors
- **Backend Gateway**: Triggers ingestion after material upload; requests relevant context chunks during case generation.
- **FastAPI AI Service**: Coordinates document parsing, chunking, embedding generation, and vector retrieval.
- **PostgreSQL + pgvector**: Stores text chunks with vector embeddings and executes cosine similarity queries.
- **LLM Embedding Provider**: Generates dense vector representations (e.g. Gemini `text-embedding-004` or OpenAI `text-embedding-3-small`).

---

## 3. Scope
- Parsing raw text from PDF and DOCX documents stored in MinIO.
- Splitting extracted text into semantic chunks with configurable overlap.
- Generating vector embeddings for each chunk via provider abstraction.
- Storing chunks and vectors in PostgreSQL with `vector(1536)` / `vector(768)` type.
- Top-K cosine similarity semantic retrieval filtered by course and material IDs.
- Enforcing the mandatory `<sources>...</sources>` untrusted data boundary.

---

## 4. Functional Requirements
- **FR-RAG-01**: The system shall parse text from PDF (via PyPDF or equivalent) and DOCX (via python-docx or equivalent).
- **FR-RAG-02**: The system shall split documents into chunks (e.g. using LangChain text splitters as an allowed/possible option, or equivalent Python splitters) with a target size (default 512 tokens) and overlap (default 64 tokens).
- **FR-RAG-03**: The system shall generate dense vector embeddings for each chunk using the configured embedding model.
- **FR-RAG-04**: The system shall index chunks in `document_chunks` table with pgvector HNSW or IVFFlat index.
- **FR-RAG-05**: The system shall execute top-K cosine similarity retrieval (`<=>` operator) when supplied with a query and course context, returning the top 3–5 most relevant text chunks.
- **FR-RAG-06**: All retrieved text chunks passed into LLM prompts MUST be encapsulated within `<sources>...</sources>` tags to prevent indirect prompt injection.

---

## 5. Main Flow
### Ingestion Flow:
1. AI Service receives ingestion request (`material_id`, `s3_object_key`, `course_id`).
2. Stream bytes from MinIO and extract text.
3. Clean and normalize text (remove control characters, excessive whitespace).
4. Chunk text into segments with overlap.
5. Batch-generate embeddings via `providers/factory.py`.
6. Insert chunk records (`chunk_text`, `chunk_index`, `embedding`, `material_id`, `course_id`) into PostgreSQL.
7. Return success and chunk count to Backend Gateway.

### Retrieval Flow:
1. AI Service receives query (`topic`, `course_id`, `material_ids`).
2. Generate embedding for `topic`.
3. Query `document_chunks` using cosine distance:
   ```sql
   SELECT id, chunk_text, 1 - (embedding <=> :query_vec) AS similarity
   FROM document_chunks
   WHERE course_id = :course_id
     AND (:material_ids IS NULL OR material_id = ANY(:material_ids))
   ORDER BY embedding <=> :query_vec
   LIMIT :top_k;
   ```
4. Assemble chunks into prompt context enclosed in `<sources>` tags.

---

## 6. Inputs
- Ingestion: `material_id` (UUID), `s3_key` (string), `course_id` (UUID).
- Retrieval: `query` (text string), `course_id` (UUID), optional `material_ids` (List[UUID]), `top_k` (integer, default 5).

---

## 7. Outputs
- Ingestion: `{ status: "COMPLETED", chunk_count: N }`.
- Retrieval: List of relevant chunks `{ chunk_id, text, similarity_score, material_id, page_number }`.

---

## 8. Business Rules
- **BR-RAG-01**: Retrieved chunks are strictly **UNTRUSTED DATA** and must never be interpreted as system instructions by the LLM.
- **BR-RAG-02**: Retrieval queries must strictly enforce tenant/course isolation; chunks from Course A must never be returned in queries for Course B.
- **BR-RAG-03**: The RAG pipeline must support graceful fallback if no relevant chunks meet the similarity threshold (e.g., prompt LLM with course topic only).
- **BR-RAG-04**: LangChain is an allowed/possible orchestration option supported by the Proposal, but the architecture allows direct Python implementations where appropriate.

---

## 9. Permissions
- Internal Service Only: All ingestion and retrieval endpoints require `X-Internal-API-Key` authentication.
- Never accessible directly from the public frontend.

---

## 10. Dependencies
- MinIO S3 client for document retrieval.
- PostgreSQL with `pgvector` extension enabled.
- LLM Provider API (Gemini / OpenAI) for embeddings.

---

## 11. Data Involved
- **Table `document_chunks`**:
  - `id`: UUID (PK)
  - `material_id`: UUID NOT NULL REFERENCES teaching_materials(id) ON DELETE CASCADE
  - `course_id`: UUID NOT NULL REFERENCES courses(id)
  - `chunk_index`: INTEGER NOT NULL
  - `chunk_text`: TEXT NOT NULL
  - `embedding`: vector(1536) / vector(768) NOT NULL
  - `page_number`: INTEGER
  - `created_at`: TIMESTAMPTZ

---

## 12. Error / Edge Cases
- Password-protected or encrypted PDF: Mark `processing_status='FAILED'` with "Encrypted PDF not supported".
- Scanned image PDF (no text layer): Return error "No extractable text found".
- Upstream Embedding API rate limit: Exponential backoff retry (up to 3 attempts).
- Corrupted document stream: Graceful failure with cleanup of orphaned chunks.

---

## 13. Out of Scope
- Hybrid search (BM25 + Dense vector reranking) in MVP.
- Complex agentic multi-hop retrieval or GraphRAG.
- Auto-summarization of entire textbook collections.

---

## 14. Related Documentation
- [`docs/requirements/REQUIREMENT-TRACEABILITY.md`](../requirements/REQUIREMENT-TRACEABILITY.md) (Items 7, 8)
- [`docs/ai/RAG-PIPELINE.md`](../ai/RAG-PIPELINE.md)
- [`docs/architecture/SERVICE-BOUNDARIES.md`](../architecture/SERVICE-BOUNDARIES.md)

---

## 15. Implementation Status
**Structurally Scaffolded**  
*(FastAPI parser and chunker stubs in `ai-service/app/ingestion/`, provider abstraction in `app/providers/`, and database pgvector extension config exist; active ingestion routes and retrieval endpoints remain unimplemented.)*
