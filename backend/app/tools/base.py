"""
Shared contract for agent tools.

Every tool in app/tools/ takes a small typed input, returns a ToolResult,
and never raises on "not found" — an empty ToolResult (found=False) is the
expected way to signal "nothing verified matches this query", which is
what powers the unknown-question handling in the orchestrator.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from app.models.schemas import Source


@dataclass
class ToolResult:
    found: bool
    content: str  # plain-text context to hand to the LLM / fallback composer
    sources: List[Source] = field(default_factory=list)
    tool_name: str = ""
