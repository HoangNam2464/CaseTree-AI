---
description: Rules for the RAG pipeline in EduBranch AI.
trigger: keyword
keywords: [rag, retrieval, embedding, pgvector, chunking, vector search, langchain]
---

# Feature Rules: RAG Pipeline

## Scope
FastAPI `ai-service/` — `ingestion/`, `retrieval/`, `generation/` packages.

## Pipeline

```
TeachingMaterial (PDF/DOCX)
    ↓ DocumentParser
    ↓ DocumentChunker (LangChain text splitters)
    ↓ EmbeddingGeneration (provider abstraction)
    ↓ pgvector storage
    ↓ Query embedding
    ↓ Metadata-filtered top-K retrieval
    ↓ Prompt construction
    ↓ <sources> boundary wrapping
    ↓ LLM generation
    ↓ Pydantic structured output validation
```

## Included
- PDF parsing (PyPDF)
- DOCX parsing (python-docx)
- Text chunking with overlap (LangChain RecursiveCharacterTextSplitter)
- Embedding generation (OpenAI or Gemini via provider abstraction)
- pgvector storage with source metadata (document_id, chunk_index, page_number)
- Top-K semantic retrieval with metadata filtering by material/course
- Citation/provenance: track source_chunk_id → document_id

## Excluded
- BM25 or hybrid retrieval — not in MVP
- Multi-step retrieval or query expansion — not in MVP
- Reranking — not in MVP
- Cross-encoder — not in MVP

## Security — CRITICAL
- Retrieved chunks are UNTRUSTED DATA
- ALL retrieved content MUST be placed inside `<sources>...</sources>` boundary in the prompt
- Retrieved content MUST NOT be able to override system instructions
- Prompt injection through uploaded documents must be mitigated

## Testing Expectations
- Unit test for chunking (correct chunk size and overlap)
- Unit test that `<sources>` boundary is always present in prompts
- Integration test for embedding → retrieval roundtrip
