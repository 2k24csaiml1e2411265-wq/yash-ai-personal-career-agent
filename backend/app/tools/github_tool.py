"""
GitHub Tool
-----------
Purpose: surface real GitHub data (public repo list, primary languages)
for the configured username. Calls the public GitHub REST API directly —
no metrics are ever invented. If the API call fails (network, rate limit,
no username configured) the tool returns found=False rather than making
up stars, followers, or repo counts.

A short in-memory cache avoids hammering the GitHub API on every chat
message or diagnostics check.
"""
from __future__ import annotations

import time
from typing import Any, Dict, List, Optional

import httpx

from app.config import settings
from app.models.schemas import Source
from app.tools.base import ToolResult

TOOL_NAME = "github_tool"

_CACHE: Dict[str, Any] = {"data": None, "fetched_at": 0.0}
_CACHE_TTL_SECONDS = 300


def _fetch_repos() -> Optional[List[Dict[str, Any]]]:
    if not settings.github_username:
        return None

    now = time.time()
    if _CACHE["data"] is not None and (now - _CACHE["fetched_at"]) < _CACHE_TTL_SECONDS:
        return _CACHE["data"]

    headers = {"Accept": "application/vnd.github+json"}
    if settings.github_token:
        headers["Authorization"] = f"Bearer {settings.github_token}"

    url = f"https://api.github.com/users/{settings.github_username}/repos"
    try:
        with httpx.Client(timeout=6.0) as client:
            resp = client.get(url, headers=headers, params={"sort": "updated", "per_page": 10})
            if resp.status_code != 200:
                return None
            data = resp.json()
            _CACHE["data"] = data
            _CACHE["fetched_at"] = now
            return data
    except Exception:
        return None


def run(query: str = "") -> ToolResult:
    try:
        repos = _fetch_repos()
        if not repos:
            return ToolResult(found=False, content="", tool_name=TOOL_NAME)

        lines = []
        for repo in repos[:6]:
            name = repo.get("name", "")
            desc = repo.get("description") or "No description provided."
            lang = repo.get("language") or "Unspecified"
            lines.append(f"- {name} ({lang}): {desc}")

        content = f"Recent public repositories for {settings.github_username}:\n" + "\n".join(lines)
        return ToolResult(
            found=True,
            content=content,
            sources=[Source(
                label="GitHub → Public repositories",
                section="github",
                url=f"https://github.com/{settings.github_username}",
            )],
            tool_name=TOOL_NAME,
        )
    except Exception:
        return ToolResult(found=False, content="", tool_name=TOOL_NAME)
