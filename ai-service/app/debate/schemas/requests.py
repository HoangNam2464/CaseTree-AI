"""
EduBranch AI — Debate Assistant API Request/Response Schemas.

IMPORTANT: The AI Debate Assistant is a Devil's Advocate tool only.
It generates targeted counter-questions. It does NOT grade students,
determine pass/fail, or make academic integrity judgments.
"""

from pydantic import BaseModel, Field
import uuid


class DebateRequest(BaseModel):
    """
    Request to generate an AI counter-question for a student argument.
    Sent by Spring Boot after a student submits their argument.
    """

    session_id: uuid.UUID = Field(..., description="Debate session ID.")
    argument_id: uuid.UUID = Field(..., description="The student argument being debated.")
    student_argument: str = Field(
        ...,
        description="The student's written justification for their decision.",
        min_length=10,
    )
    case_context: str = Field(
        ...,
        description="Relevant case node situation and option consequence for context.",
    )
    round_number: int = Field(
        ...,
        description="Current debate round (1 or 2). Max is 2.",
        ge=1,
        le=2,
    )
    retrieved_context: str = Field(
        default="",
        description="Optional: retrieved teaching material context for grounding.",
    )
    previous_exchange: list[dict] = Field(
        default_factory=list,
        description="Previous round messages for context in round 2.",
    )


class DebateResponse(BaseModel):
    """Response containing the AI-generated counter-question."""

    counter_question: str = Field(
        ...,
        description="The AI Debate Assistant's targeted counter-question.",
    )
    round_number: int
    is_final_round: bool = Field(
        ...,
        description="True if this is the last debate round (round 2). No further rounds after this.",
    )
