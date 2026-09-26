"""
Edu-Branch-AI — Unit Tests for Decision Tree Validation Schema and Graph Algorithms.
"""

import pytest
from pydantic import ValidationError
from app.generation.schemas.decision_tree import (
    CaseGenerationOutput,
    NodeOutput,
    OptionOutput,
)


def test_valid_decision_tree():
    """Verify that a valid DAG tree passes validation."""
    tree = CaseGenerationOutput(
        title="Valid Business Ethics Case",
        description="A detailed scenario testing ethical decision making in business context.",
        root_node_index=0,
        nodes=[
            NodeOutput(
                situation="Initial situation node requiring the student to choose between two paths.",
                options=[
                    OptionOutput(
                        text="Choose option 1 leading to node 1",
                        consequence="Consequence of choosing option 1.",
                        next_node_index=1,
                    ),
                    OptionOutput(
                        text="Choose option 2 leading to terminal outcome",
                        consequence="Immediate termination consequence.",
                        next_node_index=None,
                    ),
                ],
            ),
            NodeOutput(
                situation="Second node situation following option 1 choice.",
                options=[
                    OptionOutput(
                        text="Complete the case study successfully",
                        consequence="Final outcome consequence.",
                        next_node_index=None,
                    )
                ],
            ),
        ],
    )
    assert tree.root_node_index == 0
    assert len(tree.nodes) == 2


def test_cycle_detection():
    """Verify that cycles (back-edges to ancestors) are rejected."""
    with pytest.raises(ValidationError, match="Cycle detected"):
        CaseGenerationOutput(
            title="Cyclic Case Study Test",
            description="Testing that cycle detection rejects infinite loops in trees.",
            root_node_index=0,
            nodes=[
                NodeOutput(
                    situation="Root situation with one path to node 1 and one terminal exit.",
                    options=[
                        OptionOutput(
                            text="Go to node 1",
                            consequence="Going to node 1.",
                            next_node_index=1,
                        ),
                        OptionOutput(
                            text="Exit path here",
                            consequence="Terminal consequence.",
                            next_node_index=None,
                        ),
                    ],
                ),
                NodeOutput(
                    situation="Node 1 looping back to root node 0 creating an invalid cycle.",
                    options=[
                        OptionOutput(
                            text="Loop back to node 0",
                            consequence="Looping consequence.",
                            next_node_index=0,
                        )
                    ],
                ),
            ],
        )


def test_orphan_node_detection():
    """Verify that unreachable/orphan nodes are rejected."""
    with pytest.raises(ValidationError, match="Orphan node detected"):
        CaseGenerationOutput(
            title="Orphan Node Case Study Test",
            description="Testing that unreachable nodes are rejected as invalid trees.",
            root_node_index=0,
            nodes=[
                NodeOutput(
                    situation="Root situation pointing to terminal consequence directly.",
                    options=[
                        OptionOutput(
                            text="Finish case now",
                            consequence="Case finished consequence.",
                            next_node_index=None,
                        )
                    ],
                ),
                NodeOutput(
                    situation="Orphan situation node that has no incoming edges from root.",
                    options=[
                        OptionOutput(
                            text="Orphan option",
                            consequence="Orphan consequence.",
                            next_node_index=None,
                        )
                    ],
                ),
            ],
        )


def test_missing_terminal_path():
    """Verify that trees without at least one terminal path are rejected."""
    with pytest.raises(ValidationError, match="at least one terminal path"):
        CaseGenerationOutput(
            title="No Terminal Case Study Test",
            description="Testing that trees without any terminal path are rejected.",
            root_node_index=0,
            nodes=[
                NodeOutput(
                    situation="Root situation pointing to node 1 only.",
                    options=[
                        OptionOutput(
                            text="Go to node 1",
                            consequence="Going to node 1.",
                            next_node_index=1,
                        )
                    ],
                ),
                NodeOutput(
                    situation="Node 1 pointing back to node 0 with no terminal path.",
                    options=[
                        OptionOutput(
                            text="Go back to node 0",
                            consequence="Looping without terminal exit.",
                            next_node_index=0,
                        )
                    ],
                ),
            ],
        )
