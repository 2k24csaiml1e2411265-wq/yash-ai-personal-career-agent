"""
Project Tool
------------
Purpose: retrieve detailed, verified information about one of Yash's
projects, either by name/id or by matching technology/category.

Input:  a free-text query that names or describes a project
Output: ToolResult with the project's problem/solution/features/tech and
        a Source pointing at "Projects → <name>"
"""
from __future__ import annotations

import re

from app.services.knowledge_base import knowledge_base
from app.models.schemas import Source
from app.tools.base import ToolResult

TOOL_NAME = "project_tool"
_STOPWORDS = {
    "what", "which", "projects", "project", "has", "yash", "built", "build",
    "with", "using", "the", "a", "an", "and", "show", "me", "explain", "about",
}


def _format_project(p: dict) -> str:
    parts = [
        f"Project: {p['name']} ({p.get('status', 'Unknown status')})",
        f"Summary: {p.get('short_description', '')}",
        f"Problem: {p.get('problem', '')}",
        f"Solution: {p.get('solution', '')}",
        f"Key features: {', '.join(p.get('features', []))}",
        f"Technologies: {', '.join(p.get('technologies', []))}",
    ]
    return "\n".join(part for part in parts if part.strip())


def run(query: str) -> ToolResult:
    try:
        project = knowledge_base.get_project(query)
        if not project:
            # try matching by technology mentioned in the query — strip
            # punctuation and skip stopwords so "...with Python?" still
            # matches the "Python" technology tag.
            raw_tokens = re.findall(r"[A-Za-z0-9+.#]+", query)
            seen_matches = {}
            for token in raw_tokens:
                if token.lower() in _STOPWORDS or len(token) < 2:
                    continue
                for p in knowledge_base.find_projects_by_technology(token):
                    seen_matches[p["id"]] = p
            if seen_matches:
                matches = list(seen_matches.values())
                content = "\n\n---\n\n".join(_format_project(p) for p in matches)
                sources = [
                    Source(label=f"Projects → {p['name']}", section="projects",
                           ref_id=p["id"], url=f"/projects/{p['id']}")
                    for p in matches
                ]
                return ToolResult(found=True, content=content, sources=sources, tool_name=TOOL_NAME)
            return ToolResult(found=False, content="", tool_name=TOOL_NAME)

        return ToolResult(
            found=True,
            content=_format_project(project),
            sources=[Source(
                label=f"Projects → {project['name']}",
                section="projects",
                ref_id=project["id"],
                url=f"/projects/{project['id']}",
            )],
            tool_name=TOOL_NAME,
        )
    except Exception:
        # Tools never crash the agent — a failed lookup degrades to "not found".
        return ToolResult(found=False, content="", tool_name=TOOL_NAME)


def run_list_all() -> ToolResult:
    """Return a compact summary of every project — used for 'strongest project' style queries."""
    try:
        if not knowledge_base.projects:
            return ToolResult(found=False, content="", tool_name=TOOL_NAME)
        content = "\n\n---\n\n".join(_format_project(p) for p in knowledge_base.projects)
        sources = [
            Source(label=f"Projects → {p['name']}", section="projects", ref_id=p["id"], url=f"/projects/{p['id']}")
            for p in knowledge_base.projects
        ]
        return ToolResult(found=True, content=content, sources=sources, tool_name=TOOL_NAME)
    except Exception:
        return ToolResult(found=False, content="", tool_name=TOOL_NAME)
