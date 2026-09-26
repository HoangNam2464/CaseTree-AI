"""
Edu-Branch-AI — LLM Provider Factory.

Returns the configured provider based on the AI_PROVIDER environment variable.
Use this factory in route handlers and services — never instantiate providers directly.
"""

from functools import lru_cache

from app.core.config import settings
from app.providers.base import BaseLLMProvider


@lru_cache(maxsize=1)
def get_provider() -> BaseLLMProvider:
    """
    Returns the active LLM provider singleton.

    Configure via: AI_PROVIDER=openai|gemini in .env
    """
    if settings.ai_provider == "openai":
        from app.providers.openai_provider import OpenAIProvider
        return OpenAIProvider()
    elif settings.ai_provider == "gemini":
        from app.providers.gemini_provider import GeminiProvider
        return GeminiProvider()
    else:
        raise ValueError(f"Unknown AI provider: {settings.ai_provider}")
