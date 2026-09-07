"""
Links Tool
----------
Purpose: return verified contact / profile links (GitHub, LinkedIn, email,
resume). Never fabricates a URL — if a field is a TODO placeholder in the
data file, it is passed through as-is so the UI/agent can say it isn't
available yet rather than inventing one.
"""
from __future__ import annotations

from app.services.knowledge_base import knowledge_base
from app.models.schemas import Source
from app.tools.base import ToolResult

TOOL_NAME = "links_tool"


def run(query: str = "") -> ToolResult:
    try:
        links = knowledge_base.links
        if not links:
            return ToolResult(found=False, content="", tool_name=TOOL_NAME)

        lines = []
        for key, value in links.items():
            if not value:
                continue
            lines.append(f"{key.title()}: {value}")

        return ToolResult(
            found=True,
            content="\n".join(lines),
            sources=[Source(label="Links → Contact & Profiles", section="links")],
            tool_name=TOOL_NAME,
        )
    except Exception:
        return ToolResult(found=False, content="", tool_name=TOOL_NAME)
