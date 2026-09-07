"""
Certifications Tool
-------------------
Purpose: retrieve Yash's verified certifications.

Input:  free-text query
Output: ToolResult containing verified certification information
"""

from __future__ import annotations

from app.services.knowledge_base import knowledge_base
from app.models.schemas import Source
from app.tools.base import ToolResult

TOOL_NAME = "certifications_tool"


def run(query: str = "") -> ToolResult:
    try:
        if not knowledge_base.certifications:
            return ToolResult(
                found=False,
                content="",
                tool_name=TOOL_NAME,
            )

        lines = []
        sources = []

        for cert in knowledge_base.certifications:
            name = cert.get("name", "Certification")
            issuer = cert.get("issuer", "")
            date = cert.get("date", "")
            description = cert.get("description", "")
            credential_url = cert.get("credential_url", "")

            line = f"- {name}"

            if issuer:
                line += f" | Issuer: {issuer}"

            if date:
                line += f" | Date: {date}"

            if description:
                line += f" | {description}"

            if credential_url:
                line += f" | Credential: {credential_url}"

            lines.append(line)

            sources.append(
                Source(
                    label=f"Certification → {name}",
                    section="certifications",
                    ref_id=f"cert-{name}",
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
            content="Verified certifications:\n" + "\n".join(lines),
            sources=sources,
            tool_name=TOOL_NAME,
        )

    except Exception:
        return ToolResult(
            found=False,
            content="",
            tool_name=TOOL_NAME,
        )
