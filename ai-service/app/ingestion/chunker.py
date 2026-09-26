"""
Edu-Branch-AI — Document Chunker.

Splits parsed document text into overlapping chunks suitable for embedding.
Uses LangChain text splitters.

Status: Scaffolded — implementation in feature/document-processing
"""

from dataclasses import dataclass
from app.core.config import settings


@dataclass
class DocumentChunk:
    """A single text chunk from a parsed document."""
    chunk_index: int
    text: str
    document_id: str
    source_metadata: dict  # e.g. page number, section


class DocumentChunker:
    """Splits document text into overlapping chunks."""

    def __init__(
        self,
        chunk_size: int = None,
        chunk_overlap: int = None,
    ):
        self.chunk_size = chunk_size or settings.rag_chunk_size
        self.chunk_overlap = chunk_overlap or settings.rag_chunk_overlap

    def chunk(self, text: str, document_id: str, metadata: dict | None = None) -> list[DocumentChunk]:
        """
        Split text into overlapping chunks.

        Args:
            text: Full document text
            document_id: Source document UUID (for citation)
            metadata: Optional metadata (page numbers, section, etc.)

        Returns:
            List of DocumentChunk objects

        Status: TODO — implement in feature/document-processing
        """
        raise NotImplementedError("Document chunking not yet implemented")
