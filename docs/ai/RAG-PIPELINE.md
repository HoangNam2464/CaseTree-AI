# CaseTree AI — RAG Pipeline

**Status**: Scaffolded

---

## Pipeline Overview

```
TeachingMaterial (PDF / DOCX stored in MinIO)
        ↓
[1] DocumentParser        (PyPDF / python-docx)
        ↓
[2] DocumentChunker       (LangChain RecursiveCharacterTextSplitter)
        Chunk size: configurable (default 512 tokens)
        Chunk overlap: configurable (default 64 tokens)
        ↓
[3] EmbeddingGeneration   (OpenAI text-embedding-3-small | Gemini text-embedding-004)
        ↓
[4] pgvector storage      (table: document_chunks, column: embedding vector(1536))
        Store: chunk_text, chunk_index, document_id, course_id, page_number (if available)
        ↓
        [At case generation time:]
        ↓
[5] Query embedding       (same model as indexing)
        ↓
[6] Metadata filtering    (filter by material_ids or course_id)
        ↓
[7] Top-K retrieval       (pgvector cosine similarity, k=5 default)
        ↓
[8] Prompt construction
        System: "You are an expert case study author for university education..."
        <sources>
        [retrieved chunk texts]
        </sources>
        User: "Generate a branching case study on topic X..."
        ↓
[9] LLM generation        (via provider abstraction)
        ↓
[10] Pydantic validation  (CaseGenerationOutput schema)
        ↓
[11] Return to Backend Gateway for persistence
```

## Security Rules

- Retrieved chunks are UNTRUSTED DATA from uploaded documents
- ALL retrieved content MUST be enclosed in `<sources>...</sources>` boundary
- The boundary prevents source content from overriding system instructions (prompt injection mitigation)
- Never concatenate raw source text directly into the system prompt
- User-provided topic hints must be validated and sanitized

## Citation / Provenance

Each generated case should track which source chunks were used:
- `source_chunk_id` → `document_chunk.id`
- `document_id` → `teaching_material.id`
- `page_number` (if available from parser)

This enables citation traceability: case content → source chunk → original document.

## MVP Scope

- Basic top-K cosine similarity retrieval
- No reranking, BM25, query expansion, or multi-step retrieval in MVP
- Metadata filtering by course/material IDs
