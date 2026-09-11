"""
EduBranch AI — FastAPI AI Service Entry Point.

IMPORTANT: This service is INTERNAL ONLY.
It is called exclusively by the NestJS Backend Gateway.
It must NEVER be exposed directly to the internet.

All routes require X-Internal-API-Key header authentication.
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from datetime import datetime

from app.core.config import settings
from app.core.logging import configure_logging, logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown lifecycle."""
    configure_logging(debug=settings.debug)
    logger.info(
        "ai_service_startup",
        service=settings.app_name,
        version=settings.app_version,
        provider=settings.ai_provider,
    )
    yield
    logger.info("ai_service_shutdown")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "EduBranch AI — Internal FastAPI AI Service. "
        "Responsible for: document ingestion, RAG retrieval, "
        "case generation, and AI debate assistance."
    ),
    # Disable docs in production — internal service should not expose Swagger publicly
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    lifespan=lifespan,
)

# CORS: Accept only from the Backend Gateway (NestJS — internal network)
# In production, this should be restricted to the internal Docker network
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Backend Gateway only
    allow_credentials=False,
    allow_methods=["POST", "GET"],
    allow_headers=["X-Internal-API-Key", "Content-Type"],
)


# ==============================================================================
# Health endpoint — no auth required
# ==============================================================================
@app.get("/health", tags=["Health"])
async def health():
    """
    Health check endpoint.
    GET /health → 200 OK
    No authentication required.
    """
    return {
        "status": "UP",
        "service": settings.app_name,
        "version": settings.app_version,
        "provider": settings.ai_provider,
        "timestamp": datetime.utcnow().isoformat(),
    }


# ==============================================================================
# Route registration
# TODO: Uncomment as feature branches are implemented
# ==============================================================================

# from app.ingestion.router import router as ingestion_router
# from app.generation.router import router as generation_router
# from app.debate.router import router as debate_router

# app.include_router(ingestion_router, prefix="/ingestion", tags=["Ingestion"])
# app.include_router(generation_router, prefix="/generation", tags=["Generation"])
# app.include_router(debate_router, prefix="/debate", tags=["Debate"])


# ==============================================================================
# Global exception handler
# ==============================================================================
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("unhandled_exception", path=str(request.url), error=str(exc))
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal error occurred in the AI service"},
    )
