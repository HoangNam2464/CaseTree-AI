"""
EduBranch AI — Structured logging configuration.
"""

import structlog
import logging


def configure_logging(debug: bool = False) -> None:
    """Configure structlog for the AI service."""
    log_level = logging.DEBUG if debug else logging.INFO

    logging.basicConfig(
        format="%(message)s",
        level=log_level,
    )

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer() if debug else structlog.processors.JSONRenderer(),
        ],
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


logger = structlog.get_logger()
