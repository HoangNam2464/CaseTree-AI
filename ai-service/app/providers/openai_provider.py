"""
CaseTree AI — OpenAI LLM Provider Implementation.

Implements BaseLLMProvider using the OpenAI SDK.
Used when app.core.config.settings.ai_provider == "openai".
"""

import json
from typing import Any

from openai import AsyncOpenAI

from app.core.config import settings
from app.core.exceptions import ProviderException
from app.providers.base import BaseLLMProvider


class OpenAIProvider(BaseLLMProvider):
    """OpenAI provider using GPT-4o-mini / GPT-4o for generation."""

    def __init__(self) -> None:
        if not settings.openai_api_key:
            raise ProviderException("OPENAI_API_KEY is not configured")
        self._client = AsyncOpenAI(api_key=settings.openai_api_key)
        self._model = settings.openai_model
        self._embedding_model = settings.openai_embedding_model

    async def generate_text(self, prompt: str, system_prompt: str | None = None, **kwargs) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        try:
            response = await self._client.chat.completions.create(
                model=self._model,
                messages=messages,
                **kwargs,
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            raise ProviderException(f"OpenAI text generation failed: {e}") from e

    async def generate_structured(self, prompt: str, schema: dict[str, Any], system_prompt: str | None = None, **kwargs) -> dict[str, Any]:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        try:
            response = await self._client.chat.completions.create(
                model=self._model,
                messages=messages,
                response_format={"type": "json_object"},
                **kwargs,
            )
            raw = response.choices[0].message.content or "{}"
            return json.loads(raw)
        except Exception as e:
            raise ProviderException(f"OpenAI structured generation failed: {e}") from e

    async def generate_embedding(self, text: str) -> list[float]:
        try:
            response = await self._client.embeddings.create(
                model=self._embedding_model,
                input=text,
            )
            return response.data[0].embedding
        except Exception as e:
            raise ProviderException(f"OpenAI embedding failed: {e}") from e

    async def generate_embeddings_batch(self, texts: list[str]) -> list[list[float]]:
        try:
            response = await self._client.embeddings.create(
                model=self._embedding_model,
                input=texts,
            )
            return [item.embedding for item in sorted(response.data, key=lambda x: x.index)]
        except Exception as e:
            raise ProviderException(f"OpenAI batch embedding failed: {e}") from e
