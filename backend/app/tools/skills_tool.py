"""
Skills Tool
-----------
Purpose: retrieve Yash's verified technical skills, optionally filtered to
one category (programming / ai_ml / backend / cloud_data).

Input:  free-text query, may mention a category or specific technology
Output: ToolResult listing matching skill categories with sources
"""
from __future__ import annotations

from app.services.knowledge_base import knowledge_base
from app.models.schemas import Source
from app.tools.base import ToolResult

TOOL_NAME = "skills_tool"

_CATEGORY_ALIASES = {
    "programming": ["programming", "languages", "coding"],
    "ai_ml": ["ai", "ml", "machine learning", "ai/ml", "artificial intelligence"],
    "backend": ["backend", "back-end", "server", "web"],
    "cloud_data": ["cloud", "data", "gcp", "kubernetes", "bigquery"],
}


def run(query: str = "") -> ToolResult:
    try:
        if not knowledge_base.skills:
            return ToolResult(found=False, content="", tool_name=TOOL_NAME)

        query_l = query.strip().lower()
        matched_categories = [
            cat for cat, aliases in _CATEGORY_ALIASES.items()
            if any(alias in query_l for alias in aliases)
        ]
        categories = matched_categories if matched_categories else list(knowledge_base.skills.keys())

        lines, sources = [], []
        for cat in categories:
            items = knowledge_base.skills.get(cat, [])
            if not items:
                continue
            label = cat.replace("_", " ").title()
            lines.append(f"{label}: {', '.join(items)}")
            sources.append(Source(label=f"Skills → {label}", section="skills", ref_id=cat))

        if not lines:
            return ToolResult(found=False, content="", tool_name=TOOL_NAME)

        return ToolResult(found=True, content="\n".join(lines), sources=sources, tool_name=TOOL_NAME)
    except Exception:
        return ToolResult(found=False, content="", tool_name=TOOL_NAME)
