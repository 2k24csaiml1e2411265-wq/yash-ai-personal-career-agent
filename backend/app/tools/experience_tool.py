"""
Experience Tool
----------------
Purpose: retrieve verified internship / work experience information.

Input:  free-text query (may name an organization, or be generic like
        "internships")
Output: ToolResult summarizing matching experience entries with sources
"""
from __future__ import annotations

from app.services.knowledge_base import knowledge_base
from app.models.schemas import Source
from app.tools.base import ToolResult

TOOL_NAME = "experience_tool"


def _format_experience(e: dict) -> str:
    parts = [
        f"{e['role']} at {e['organization']} ({e.get('duration', '')}, {e.get('location', '')})",
        e.get("description", ""),
        f"Technologies: {', '.join(e.get('technologies', []))}",
        "Highlights: " + "; ".join(e.get("highlights", [])),
    ]
    return "\n".join(part for part in parts if part.strip())


def run(query: str = "") -> ToolResult:
    try:
        if not knowledge_base.experience:
            return ToolResult(found=False, content="", tool_name=TOOL_NAME)

        query_l = query.strip().lower()
        matches = [
            e for e in knowledge_base.experience
            if query_l and (query_l in e["organization"].lower() or query_l in e["role"].lower())
        ]
        entries = matches if matches else knowledge_base.experience

        content = "\n\n---\n\n".join(_format_experience(e) for e in entries)
        sources = [
            Source(label=f"Experience → {e['organization']}", section="experience", ref_id=e["id"])
            for e in entries
        ]
        return ToolResult(found=True, content=content, sources=sources, tool_name=TOOL_NAME)
    except Exception:
        return ToolResult(found=False, content="", tool_name=TOOL_NAME)
