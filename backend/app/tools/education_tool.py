"""
Education Tool
--------------
Purpose: retrieve Yash's verified educational background.
"""

from __future__ import annotations

from app.models.schemas import Source
from app.services.knowledge_base import knowledge_base
from app.tools.base import ToolResult

TOOL_NAME = "education_tool"


def run(query: str = "") -> ToolResult:
    try:
        education = knowledge_base.education

        if not education:
            return ToolResult(
                found=False,
                content="",
                tool_name=TOOL_NAME,
            )

        lines = []
        sources = []

        for item in education:
            parts = []

            for key, value in item.items():
                if value in (None, "", []):
                    continue

                label = key.replace("_", " ").title()

                if isinstance(value, list):
                    value = ", ".join(str(v) for v in value)

                parts.append(f"{label}: {value}")

            if parts:
                lines.append("\n".join(parts))

            sources.append(
                Source(
                    label="Education",
                    section="education",
                    ref_id="education",
                )
            )

        if not lines:
            return ToolResult(
                found=False,
                content="",
                tool_name=TOOL_NAME,
            )

        return ToolResult(
            found=True,
            content="Verified educational background:\n\n"
            + "\n\n---\n\n".join(lines),
            sources=sources,
            tool_name=TOOL_NAME,
        )

    except Exception:
        return ToolResult(
            found=False,
            content="",
            tool_name=TOOL_NAME,
        )