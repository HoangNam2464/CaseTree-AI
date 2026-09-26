"""
Edu-Branch-AI — Decision Tree Case JSON Schema and Pydantic Models.

These Pydantic models define the STRUCTURED OUTPUT contract for the AI Case Generator.
The LLM must produce output conforming to this schema (validated by the AI service
before forwarding to the Backend Gateway (NestJS)).

Structure:
  CaseGenerationOutput
    └── nodes: list[NodeOutput]
           └── options: list[OptionOutput]
                    └── next_node_index: int | None (index into nodes array)

INVARIANTS enforced at validation:
  - root_node_index must be a valid index
  - At least one terminal node (option with next_node_index=None)
  - No orphan nodes (every non-root node reachable from root)
  - No cycles (enforced by depth-limited BFS validation)
"""

from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field, model_validator


class OptionOutput(BaseModel):
    """A decision option at a case node."""

    text: str = Field(
        ...,
        description="The decision choice text shown to the student.",
        min_length=5,
    )
    consequence: str = Field(
        ...,
        description="The immediate consequence displayed after the student selects this option.",
        min_length=10,
    )
    next_node_index: Optional[int] = Field(
        None,
        description="Index into the nodes array for the next node. None = terminal path.",
        ge=0,
    )


class NodeOutput(BaseModel):
    """A situation node in the decision tree."""

    situation: str = Field(
        ...,
        description="The situation/scenario text presented to the student at this decision point.",
        min_length=20,
    )
    options: list[OptionOutput] = Field(
        default_factory=list,
        description="Decision options available at this node. Empty list = terminal node.",
    )

    @property
    def is_terminal(self) -> bool:
        """A node is terminal if it has no options."""
        return len(self.options) == 0


class CaseGenerationOutput(BaseModel):
    """
    Structured output contract for the Edu-Branch-AI Case Generator.

    The LLM must produce a JSON object conforming to this schema.
    This is validated by the AI service before forwarding to the Backend Gateway (NestJS).
    """

    title: str = Field(..., description="Case study title.", min_length=5)
    description: str = Field(..., description="Brief description of the case context.", min_length=20)
    root_node_index: int = Field(
        0,
        description="Index of the root node in the nodes array. Defaults to 0.",
        ge=0,
    )
    nodes: list[NodeOutput] = Field(
        ...,
        description="All nodes in the decision tree.",
        min_length=2,
    )

    @model_validator(mode="after")
    def validate_tree_structure(self) -> CaseGenerationOutput:
        """Validate the decision tree for structural integrity."""
        n = len(self.nodes)

        if self.root_node_index >= n:
            raise ValueError(f"root_node_index={self.root_node_index} is out of range (nodes count={n})")

        # Collect all referenced next_node indices
        all_next_indices: set[int] = set()
        for node in self.nodes:
            for opt in node.options:
                if opt.next_node_index is not None:
                    if opt.next_node_index >= n:
                        raise ValueError(
                            f"next_node_index={opt.next_node_index} is out of range (nodes count={n})"
                        )
                    all_next_indices.add(opt.next_node_index)

        # Check for at least one terminal node
        has_terminal = any(node.is_terminal for node in self.nodes)
        if not has_terminal:
            # Also check if any option has next_node_index=None
            has_terminal_option = any(
                opt.next_node_index is None
                for node in self.nodes
                for opt in node.options
            )
            if not has_terminal_option:
                raise ValueError("Decision tree must have at least one terminal path (option with next_node_index=None or node with no options)")

        # Structural integrity: cycle detection and reachability (no orphan nodes)
        self._check_tree_integrity(n)

        return self

    def _check_tree_integrity(self, n: int) -> None:
        """
        Verify structural integrity of the directed graph:
        1. Cycle detection using DFS 3-color algorithm (WHITE=0, GRAY=1, BLACK=2).
           A back-edge pointing to a GRAY (currently visiting ancestor) node indicates a cycle.
        2. Reachability validation: every non-root node must be reachable from root_node_index.
           Any node remaining WHITE (unvisited) after DFS from root is an unreachable orphan node.
        """
        WHITE, GRAY, BLACK = 0, 1, 2
        colors = [WHITE] * n

        def dfs(u: int) -> None:
            colors[u] = GRAY
            for opt in self.nodes[u].options:
                v = opt.next_node_index
                if v is not None:
                    if colors[v] == GRAY:
                        raise ValueError(f"Cycle detected in decision tree involving node index {v}")
                    if colors[v] == WHITE:
                        dfs(v)
            colors[u] = BLACK

        # Run DFS traversal starting from root node
        dfs(self.root_node_index)

        # Check reachability: all nodes must have been visited (BLACK)
        for i, color in enumerate(colors):
            if color == WHITE:
                raise ValueError(
                    f"Orphan node detected: node index {i} is unreachable from root node {self.root_node_index}"
                )


# JSON Schema for LLM structured output (passed to provider.generate_structured)
CASE_GENERATION_JSON_SCHEMA = CaseGenerationOutput.model_json_schema()
