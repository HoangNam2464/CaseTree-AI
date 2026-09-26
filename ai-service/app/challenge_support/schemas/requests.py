"""
Edu-Branch-AI — AI Reasoning/Challenge Support API Request/Response Schemas.
Source of Truth: Proposal V1.1 (C1SE_65-CaseTree-AI-Proposal_V1_1.docx)

IMPORTANT: AI Reasoning/Challenge Support generates challenge/counter-questions only.
It supports both Branching Study reasoning and Review Study reasoning/solutions.
It does NOT grade students, score reasoning, determine pass/fail,
or make academic judgments. Limited to 1-2 rounds maximum.
"""

from pydantic import BaseModel, Field
from typing import Optional
import uuid


class ChallengeRequest(BaseModel):
    """
    Request to generate an AI challenge counter-question for student reasoning.
    Sent by the NestJS Backend Gateway after a student submits their reasoning.
    Supports both Branching Study and Review Study.
    """

    session_id: uuid.UUID = Field(..., description="Challenge support session ID.")
    reasoning_id: Optional[uuid.UUID] = Field(
        default=None,
        description="Branching Study student reasoning ID (if Branching Study).",
    )
    review_submission_id: Optional[uuid.UUID] = Field(
        default=None,
        description="Review Study submission ID (if Review Study).",
    )
    student_reasoning: str = Field(
        ...,
        description="The student's written reasoning or proposed solution.",
        min_length=10,
    )
    case_context: str = Field(
        ...,
        description="Relevant case situation/problem context for grounding.",
    )
    round_number: int = Field(
        ...,
        description="Current challenge round (1 or 2). Max is 2.",
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


class ChallengeResponse(BaseModel):
    """Response containing the AI-generated challenge counter-question."""

    counter_question: str = Field(
        ...,
        description="The AI Reasoning/Challenge Support targeted counter-question.",
    )
    round_number: int = Field(
        ...,
        description="Current challenge round number (1 or 2).",
    )
    is_final_round: bool = Field(
        ...,
        description="True if this is the last challenge round (round 2). No further rounds after this.",
    )
