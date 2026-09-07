"""
Profile Tool
------------
Purpose: retrieve Yash's verified personal/profile information.
"""

from __future__ import annotations

from app.models.schemas import Source
from app.services.knowledge_base import knowledge_base
from app.tools.base import ToolResult

TOOL_NAME = "profile_tool"


def run(query: str = "") -> ToolResult:
    try:
        profile = knowledge_base.profile

        if not profile:
            return ToolResult(
                found=False,
                content="",
                tool_name=TOOL_NAME,
            )

        lines = []

        name = profile.get("name")
        if name:
            lines.append(f"Name: {name}")

        for key, value in profile.items():
            if key == "name" or value in (None, "", []):
                continue

            label = key.replace("_", " ").title()

            if isinstance(value, list):
                value = ", ".join(str(item) for item in value)

            lines.append(f"{label}: {value}")

        if not lines:
            return ToolResult(
                found=False,
                content="",
                tool_name=TOOL_NAME,
            )

        return ToolResult(
            found=True,
            content="\n".join(lines),
            sources=[
                Source(
                    label="About → Profile",
                    section="profile",
                    ref_id="profile",
                )
            ],
            tool_name=TOOL_NAME,
        )

    except Exception:
        return ToolResult(
            found=False,
            content="",
            tool_name=TOOL_NAME,
        )