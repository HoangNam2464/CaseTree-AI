"""
EduBranch AI — Custom Exception Types for the AI Service.
"""


class ProviderException(Exception):
    """Raised when an LLM provider call fails."""


class DocumentParsingException(Exception):
    """Raised when a document cannot be parsed."""


class EmbeddingException(Exception):
    """Raised when embedding generation fails."""


class RetrievalException(Exception):
    """Raised when vector retrieval fails."""


class CaseGenerationException(Exception):
    """Raised when case generation fails or produces invalid output."""


class DebateAssistantException(Exception):
    """Raised when the debate assistant fails to generate a counter-question."""
