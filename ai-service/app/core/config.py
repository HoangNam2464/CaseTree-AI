"""
CaseTree AI — FastAPI Core Configuration

All configuration is loaded from environment variables.
Never hardcode secrets or API keys here.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


class Settings(BaseSettings):
    """Application settings loaded from environment variables / .env file."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # =========================================================================
    # Application
    # =========================================================================
    app_name: str = "CaseTree AI — FastAPI AI Service"
    app_version: str = "0.0.1"
    debug: bool = False

    # =========================================================================
    # Security — Internal API Key
    # AI Service is INTERNAL ONLY. Never expose to the internet.
    # =========================================================================
    ai_service_api_key: str = "changeme_internal_ai_service_api_key"

    # =========================================================================
    # Database — PostgreSQL + pgvector
    # =========================================================================
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "casetree_ai"
    postgres_user: str = "casetree"
    postgres_password: str = "changeme_db_password"

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    # =========================================================================
    # LLM Provider
    # =========================================================================
    ai_provider: Literal["openai", "gemini"] = "gemini"

    # OpenAI
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    openai_embedding_model: str = "text-embedding-3-small"

    # Google Gemini
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.0-flash"
    gemini_embedding_model: str = "text-embedding-004"

    # =========================================================================
    # RAG Configuration
    # =========================================================================
    rag_chunk_size: int = 512
    rag_chunk_overlap: int = 64
    rag_top_k: int = 5

    # =========================================================================
    # Debate Assistant
    # =========================================================================
    debate_max_rounds: int = 2


# Singleton settings instance
settings = Settings()
