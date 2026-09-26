"""
Edu-Branch-AI — FastAPI Internal Service Security

Validates the internal API key used for Backend Gateway ? Internal AI Service communication.
This service is NOT exposed to the internet.
All requests must include the X-Internal-API-Key header.
"""

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from app.core.config import settings

API_KEY_HEADER = APIKeyHeader(name="X-Internal-API-Key", auto_error=False)


def verify_internal_api_key(api_key: str = Security(API_KEY_HEADER)) -> str:
    """
    Dependency: validates the internal API key.
    Raise 403 if key is missing or invalid.
    """
    if not api_key or api_key != settings.ai_service_api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing internal API key",
        )
    return api_key
