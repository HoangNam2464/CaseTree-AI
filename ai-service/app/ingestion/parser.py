"""
Edu-Branch-AI — Document Parser.

Parses PDF and DOCX teaching material files into plain text.
Uses PyPDF for PDF parsing and python-docx for DOCX parsing.

Status: Scaffolded — implementation in feature/document-processing
"""

from pathlib import Path
from app.core.exceptions import DocumentParsingException
from app.core.logging import logger


class DocumentParser:
    """Parses PDF and DOCX files into text."""

    SUPPORTED_MIME_TYPES = {
        "application/pdf": "_parse_pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "_parse_docx",
    }

    def parse(self, file_path: Path, mime_type: str) -> str:
        """
        Parse a document file into plain text.

        Args:
            file_path: Path to the downloaded file from MinIO
            mime_type: MIME type of the document

        Returns:
            Extracted plain text

        Raises:
            DocumentParsingException: if parsing fails or MIME type is unsupported
        """
        handler_name = self.SUPPORTED_MIME_TYPES.get(mime_type)
        if not handler_name:
            raise DocumentParsingException(f"Unsupported MIME type: {mime_type}")

        handler = getattr(self, handler_name)
        logger.info("parsing_document", mime_type=mime_type, path=str(file_path))
        return handler(file_path)

    def _parse_pdf(self, file_path: Path) -> str:
        # TODO: implement in feature/document-processing
        raise NotImplementedError("PDF parsing not yet implemented")

    def _parse_docx(self, file_path: Path) -> str:
        # TODO: implement in feature/document-processing
        raise NotImplementedError("DOCX parsing not yet implemented")
