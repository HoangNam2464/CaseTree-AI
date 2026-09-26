"""
Edu-Branch-AI — LLM Provider Abstraction Base.

RULE: Route handlers and orchestration code MUST use this abstraction.
Never import openai or google.generativeai SDKs directly in route handlers.
Vendor-specific logic stays inside provider implementations.
"""

from abc import ABC, abstractmethod
from typing import Any


class BaseLLMProvider(ABC):
    """Abstract base class for all LLM providers."""

    @abstractmethod
    async def generate_text(self, prompt: str, system_prompt: str | None = None, **kwargs) -> str:
        """
        Generate text from the LLM.

        Args:
            prompt: The user/task prompt
            system_prompt: Optional system-level instructions
            **kwargs: Provider-specific options (temperature, max_tokens, etc.)

        Returns:
            Generated text string
        """

    @abstractmethod
    async def generate_structured(self, prompt: str, schema: dict[str, Any], system_prompt: str | None = None, **kwargs) -> dict[str, Any]:
        """
        Generate structured JSON output validated against a schema.

        Args:
            prompt: The generation prompt
            schema: JSON Schema dict for structured output validation
            system_prompt: Optional system instructions

        Returns:
            Validated dict conforming to schema
        """

    @abstractmethod
    async def generate_embedding(self, text: str) -> list[float]:
        """
        Generate a vector embedding for the given text.

        Args:
            text: Text to embed

        Returns:
            List of floats representing the embedding vector
        """

    @abstractmethod
    async def generate_embeddings_batch(self, texts: list[str]) -> list[list[float]]:
        """
        Generate embeddings for a batch of texts (more efficient than calling one-by-one).

        Args:
            texts: List of text strings

        Returns:
            List of embedding vectors
        """
