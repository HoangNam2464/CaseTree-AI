"""
Edu-Branch-AI — Google Gemini LLM Provider Implementation.

Implements BaseLLMProvider using the Google Generative AI SDK.
Used when app.core.config.settings.ai_provider == "gemini".
"""

import json
from typing import Any

import google.generativeai as genai

from app.core.config import settings
from app.core.exceptions import ProviderException
from app.providers.base import BaseLLMProvider


class GeminiProvider(BaseLLMProvider):
    """Google Gemini provider using Gemini Flash for generation."""

    def __init__(self) -> None:
        if not settings.gemini_api_key:
            raise ProviderException("GEMINI_API_KEY is not configured")
        genai.configure(api_key=settings.gemini_api_key)
        self._model_name = settings.gemini_model
        self._embedding_model = settings.gemini_embedding_model

    async def generate_text(self, prompt: str, system_prompt: str | None = None, **kwargs) -> str:
        try:
            model = genai.GenerativeModel(
                model_name=self._model_name,
                system_instruction=system_prompt,
            )
            response = await model.generate_content_async(prompt)
            return response.text or ""
        except Exception as e:
            raise ProviderException(f"Gemini text generation failed: {e}") from e

    async def generate_structured(self, prompt: str, schema: dict[str, Any], system_prompt: str | None = None, **kwargs) -> dict[str, Any]:
        try:
            model = genai.GenerativeModel(
                model_name=self._model_name,
                system_instruction=system_prompt,
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json",
                    response_schema=schema,
                ),
            )
            response = await model.generate_content_async(prompt)
            return json.loads(response.text or "{}")
        except Exception as e:
            raise ProviderException(f"Gemini structured generation failed: {e}") from e

    async def generate_embedding(self, text: str) -> list[float]:
        try:
            result = await genai.embed_content_async(
                model=self._embedding_model,
                content=text,
                task_type="retrieval_document",
            )
            return result["embedding"]
        except Exception as e:
            raise ProviderException(f"Gemini embedding failed: {e}") from e

    async def generate_embeddings_batch(self, texts: list[str]) -> list[list[float]]:
        try:
            results = []
            for text in texts:
                result = await genai.embed_content_async(
                    model=self._embedding_model,
                    content=text,
                    task_type="retrieval_document",
                )
                results.append(result["embedding"])
            return results
        except Exception as e:
            raise ProviderException(f"Gemini batch embedding failed: {e}") from e
