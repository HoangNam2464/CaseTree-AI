"""
Edu-Branch-AI — Unit Tests for Challenge Support Schemas and Round Constraints.
"""

import uuid
import pytest
from pydantic import ValidationError
from app.challenge_support.schemas.requests import ChallengeRequest, ChallengeResponse


def test_valid_challenge_request_branching_study():
    """Verify valid request for Branching Study student reasoning."""
    req = ChallengeRequest(
        session_id=uuid.uuid4(),
        reasoning_id=uuid.uuid4(),
        student_reasoning="I decided to terminate the contract immediately due to human rights violations.",
        case_context="The company detected severe labor abuses at a critical tier-1 supplier.",
        round_number=1,
    )
    assert req.round_number == 1
    assert req.review_submission_id is None
    assert req.reasoning_id is not None


def test_valid_challenge_request_review_study():
    """Verify valid request for Review Study student submission."""
    req = ChallengeRequest(
        session_id=uuid.uuid4(),
        review_submission_id=uuid.uuid4(),
        student_reasoning="My proposed solution is to negotiate a 60-day corrective action plan.",
        case_context="Supplier audit revealed overtime non-compliance.",
        round_number=2,
    )
    assert req.round_number == 2
    assert req.reasoning_id is None
    assert req.review_submission_id is not None


def test_round_number_bounds():
    """Verify that round_number is strictly bounded between 1 and 2."""
    with pytest.raises(ValidationError):
        ChallengeRequest(
            session_id=uuid.uuid4(),
            reasoning_id=uuid.uuid4(),
            student_reasoning="Valid student reasoning text here.",
            case_context="Valid case context.",
            round_number=0,  # Invalid: must be >= 1
        )

    with pytest.raises(ValidationError):
        ChallengeRequest(
            session_id=uuid.uuid4(),
            reasoning_id=uuid.uuid4(),
            student_reasoning="Valid student reasoning text here.",
            case_context="Valid case context.",
            round_number=3,  # Invalid: must be <= 2
        )


def test_challenge_response():
    """Verify valid challenge response schema."""
    resp = ChallengeResponse(
        counter_question="What are the immediate supply chain disruption implications of that choice?",
        round_number=1,
        is_final_round=False,
    )
    assert resp.round_number == 1
    assert not resp.is_final_round
